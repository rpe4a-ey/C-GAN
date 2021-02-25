$(document).ready(function() {
  $("button#submit").click(function(e){
    e.preventDefault();

    // var formData = new FormData();
    // formData.append('image', $('#image_file')[0].files[0]); // request.files['image']

    // $.post({
    //   url : '/api/photo',
    //   contentType: 'text/plain',
    //   data : $('input[name=input]').val(),
    //   success : function(data) {
    //     // console.log("test ok!")
    //     $('#result').text(data)
    //   },
    //   error: function(err) {
    //     console.log(err)
    //   }
    // });

    $.post({
      url : '/api/photo',
      contentType: 'text/plain',
      data : $('input[name=input]').val(),
      success : function(data) {
        console.log("success!")
        data.forEach((item, i) => {
          $('#gen_img' + (i+1)).attr('src', item)
        })
      },
       error: function(err) {
         console.log(err)
       }
    });
  });
});
