from flask import Flask, request, send_file, send_from_directory, jsonify
from flask_cors import CORS
import base64
from PIL import Image
import numpy as np
from io import BytesIO
from tensorflow import keras



app = Flask(__name__, static_url_path='')
cors = CORS(app) 

@app.route('/api/photo', methods=['POST'])
def photo():
    inp = request.data.decode('utf-8')

    model = keras.models.load_model('model', compile=False)

    images = []
    imgs_enc = []
    for i in inp:
        # arr = np.random.randint(0, 255, (num_tiles, num_tiles, 3))
        # pil_img = Image.fromarray(arr, mode='RGB')
        # buff = BytesIO()
        # pil_img.save(buff, format="PNG")
        noise_class = np.zeros((16, 10))
        class_label = int(i)
        noise_class[:,class_label] = 1

        prediction = model.predict([np.random.uniform(-1.0, 1.0, size=[16, 100]), noise_class])[0].reshape(28, 28)

        pil_img = Image.fromarray(np.uint8(prediction*255)).convert('RGB')

        images.append(pil_img)

    
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    # new_im.save('test.jpg')

    buff = BytesIO()
    new_im.save(buff, format="PNG")
    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
    gen_img =  f"data:image/png;base64, {new_image_string}"
    imgs_enc.append(gen_img)
    return jsonify(imgs_enc)

@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
