'use strict'
var contentType = 'text';
var visibility = 'public';
var description = "";
var title = "";
var form_data = new FormData();



//Preloader
var preloader = $('#spinner-wrapper');
$(window).on('load', function() {
    var preloaderFadeOutTime = 500;

    function hidePreloader() {
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
});

// helper function to get csrf token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// display selected local image
function readImg(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
          $('#uploadImg')
              .attr('src', e.target.result)
              .width(360)
              .height(400);
      };

        reader.readAsDataURL(input.files[0]);
    }
}

$( document ).ready(function() {

    // get csrftoken, used in AJAX Request
    const csrftoken = getCookie('csrftoken');
    // console.log("csrftoken = ", csrftoken);


    // deal with 2 dropdown lists: visibility and contentType
    $('div.dropdown-content a').click(function(e)
      {
       var id = $(this).attr("id")
       var icon = $(this).find("i").attr("class");
       console.log(icon);
       if (id == "public" || id == "private" || id == "friend"){
         $("#visibility").find('i').attr("class", icon);
         visibility = id;
       } else {
         $("#contentType").find('i').attr("class", icon);
         contentType = id;

         // handle upload button
         if (id == "image"){
           $("#imageFile").attr("style", "display: block");
         } else {
           $("#imageFile").attr("style", "display: none");

         }
       }
    });


    // deal with edit button
    // show textarea and hide p
    $('body').on('click', 'a.editBtn', function(e) {
      e.preventDefault();

      var content_holder = $(this).closest('.post-detail').find('p')


      $(this).closest('.post-detail').find('.edit-block').attr("style", "display: block");
      content_holder.attr("style", "display: none");
    });



    // REQUEST POST: make_post
    // create a new post
    $('#publishBtn').click(function(e){

      title = $('#title').val();
      description = $('#description').val();
      console.log("title = ", title);

      // handle file upload
      // file is stored as form data
      if (contentType == "image"){
        var file_data = $('#imageFile').prop('files')[0];
        form_data.append('file', file_data);
      }

      form_data.append("contentType", contentType);
      form_data.append("visibility", visibility);
      form_data.append("title", title);
      form_data.append("description", description);
      form_data.append("csrfmiddlewaretoken", csrftoken);


      $.ajax({
        url : "make_post/", // the endpoint
        type : "POST", // http method
        dataType: 'text', // what to expect back from the server
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,

        // handle a successful response
        success : function(json) {
            console.log("success"); // sanity check
        },
      });
    });

});
