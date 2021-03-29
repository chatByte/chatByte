'use strict'
var contentType = 'text';
var visibility = 'public';
var description = "";
var title = "";
var form_data = new FormData();
var edit_form_data = new FormData();
var x_server = window.location.origin;




function search(){
  var input = document.getElementById("search_user_input");
  var id = input.value;
  console.log(id);


$.ajax({
        url : "../search/", // the endpoint
        type : "POST", // http method
        dataType: 'text', // what to expect back from the server
        cache: false,
        headers: {"X-Server": window.location.origin},
        contentType: "application/json",
        processData: false,
        beforeSend: function(xhr) {
          console.log("why");
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
          xhr.setRequestHeader("X-Request-User", id);
        },



        data: JSON.stringify({
            url: id,
        }),


        success: function(json) {
            console.log("success"); // sanity check
            console.log("haha");
            console.log(json);
            var url = json["url"];


            window.location.replace(url);
        }, 
      }); 

} 
      // title = $('#title').val();
      // description = $('#description').val();
      // console.log("title = ", title);

      // // handle file upload
      // // file is stored as form data
      // if (contentType == "image"){
      //   var file_data = $('#imageFile').prop('files')[0];
      //   form_data.append('file', file_data);
      // }

      // form_data.append("contentType", contentType);
      // form_data.append("visibility", visibility);
      // form_data.append("title", title);
      // form_data.append("description", description);
      // form_data.append("csrfmiddlewaretoken", csrftoken);
      // var x_server = window.location.origin

      // console.log("description");
      // $.ajax({
      //   url : ".", // the endpoint
      //   // header
      //   headers: {"X-Server": x_server},
      //   beforeSend: function(xhr) {
      //     xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      //   },
      //   type : "POST", // http method
      //   dataType: 'text', // what to expect back from the server
      //   cache: false,
      //   contentType: false,
      //   processData: false,
      //   data: form_data,

      //   // handle a successful response
      //   success : function(json) {
      //       console.log("success"); // sanity check
      //       window.location.reload();
      //   },
      // });









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

function deletePost(id){
  console.log(id);
  var post_id = id.split("posts/")[1]
  console.log("Post id: ", post_id)
  var url = "../posts/"+post_id+"/";
  console.log(url);
  var csrftoken = getCookie('csrftoken');
  console.log(csrftoken);
  var x_server = id.split("author")[0]

  $.ajax({
        url : url, // the endpoint
        type : "DELETE", // http method
        dataType: 'text', // what to expect back from the server
        cache: false,
        headers: {"X-Server": x_server},
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        contentType: false,
        processData: false,

        data: {},

        // handle a successful response
        success : function(json) {
            console.log("success"); // sanity check
            location.reload();
        },
      });
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
    console.log("csrftoken = ", csrftoken);


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

      content_holder.attr("style", "display: none");
      var div_content = $('div .form-group-col').html();
      var new_div = $(this).closest('.post-detail').find('div .editText')
      new_div.attr("style", "display: block");
      new_div.html(div_content);

      // show submit btn, hide edit btn
      $(this).attr("style", "display: none");
      $(this).closest('div .edit').find('.submitBtn').attr("style", "display: block");

    });





    // deal with submit edit button
    // submit form data
    $('#submitEdit').click(function(e){

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
      var x_server = window.location.origin


      $.ajax({
        url : ".", // the endpoint
        type : "POST", // http method
        // header
        headers: {"X-Server": x_server},
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        dataType: 'text', // what to expect back from the server
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,

        // handle a successful response
        success : function(json) {
            console.log("success"); // sanity check
            window.location.reload();
        },
      });

      // $.ajax({
      //   url : ".", // the endpoint
      //   type : "DELETE", // http method
      //   dataType: 'text', // what to expect back from the server
      //   cache: false,
      //   contentType: false,
      //   processData: false,
      //   data: form_data,

      //   // handle a successful response
      //   success : function(json) {
      //       console.log("success"); // sanity check
      //   },
      // });


    });









    // REQUEST POST: make_post
    // create a new post
    $('#publishBtn').click(function(e){
      console.log(e);

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
      var x_server = window.location.origin

      console.log("description");
      $.ajax({
        url : ".", // the endpoint
        // header
        headers: {"X-Server": x_server},
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        },
        type : "POST", // http method
        dataType: 'text', // what to expect back from the server
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,

        // handle a successful response
        success : function(json) {
            console.log("success"); // sanity check
            window.location.reload();
        },
      });

      // $.ajax({
      //   url : ".", // the endpoint
      //   type : "DELETE", // http method
      //   dataType: 'text', // what to expect back from the server
      //   cache: false,
      //   contentType: false,
      //   processData: false,
      //   data: form_data,

      //   // handle a successful response
      //   success : function(json) {
      //       console.log("success"); // sanity check
      //   },
      // });


    });

});
