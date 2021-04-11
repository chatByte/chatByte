'use strict'
var contentType = 'text/plain';
var visibility = 'public';
var description = "";
var unlisted = "false";
var categories = "empty";
var title = "";
var form_data = new FormData();

var edit_form_data = new FormData();
var x_server = window.location.origin;

function search(){
  var input = document.getElementById("search_user_input");
  var id = input.value;
  var host = id.split("/");
  var host_name = host[0]+"//"+host[2]+"/";


$.ajax({
        url : "../search/", // the endpoint
        type : "POST", // http method
        dataType: 'json', // what to expect back from the server
        cache: false,
        headers: {"X-Server": host_name},
        contentType: "application/json",
        processData: false,
        beforeSend: function(xhr) {
          console.log("why");
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
          xhr.setRequestHeader("X-Request-User", id);
        },
        data: JSON.stringify({"url": id}),


        // handle a successful response
        success: function(json) {
            console.log("success"); // sanity check
            console.log("haha");
            console.log(json);
            var url = json["url"];


            window.location.replace(url);
        },
      });

}


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
  var url = "../posts/"+post_id;
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
          xhr.setRequestHeader("X-Request-User", id);
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



    // deal with submit edit button
    // submit form data
function editPost(POST_ID) {



      var id = POST_ID.split('/posts/')[1];
      console.log('aaa' + POST_ID)
      title = $("#title1").val();
      description = $("#description1").val();
      console.log("title = ", title);
      console.log("des = ", description);
      var x_server = window.location.origin
      var csrftoken = getCookie('csrftoken');

      // handle file upload
      // file is stored as form data
      if (contentType == "image1"){
        var file_data = $('#imageFile1').prop('files')[0];
        edit_form_data.append('file', file_data);

      }

      edit_form_data.append("contentType", contentType);
      edit_form_data.append("title", title);
      edit_form_data.append("description", description);
      edit_form_data.append("csrfmiddlewaretoken", csrftoken);

      $.ajax({
        // url : ".", // the endpoint
        url:"./" + id + "/edit/",
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
        data: edit_form_data,

        // handle a successful response
        success : function(json) {
            console.log("success"); // sanity check
            window.location.reload();
        },
      });
    }

    // function editButton(title, description) {
    //   $('body').on('click', 'a.editBtn', function(e) {
    //     e.preventDefault();
    //
    //     var content_holder = $(this).closest('.post-detail').find('p');
    //
    //     content_holder.attr("style", "display: none");
    //     var div_content = $('div .form-group-col').clone();
    //     var find_element = div_content.find('#title');
    //     var find_description = div_content.find('#description');
    //     find_element.attr("id", "editTitle");
    //     find_element.text(title);
    //
    //     find_description.attr("id", "editDescription");
    //     find_description.text(description);
    //
    //     // console.log(find_element);
    //     var new_div = $(this).closest('.post-detail').find('div .editText')
    //     new_div.attr("style", "display: block");
    //     new_div.html(div_content.html());
    //
    //
    //     // show submit btn, hide edit btn
    //     $(this).attr("style", "display: none");
    //     $(this).closest('div .edit').find('.submitBtn').attr("style", "display: block");
    //
    //   });
    //
    // }



// ===========================

$( document ).ready(function() {

    // get csrftoken, used in AJAX Request
    const csrftoken = getCookie('csrftoken');
    console.log("csrftoken = ", csrftoken);


    // deal with 2 dropdown lists: visibility and contentType
    $('div.dropdown-content a').click(function(e)
      {
       var id = $(this).attr("id")
       var icon = $(this).find("i").attr("class");

       switch (id) {
          case "public":
          case "private":
          case "friend":
            $("#visibility").find('i').attr("class", icon);
            visibility = id;
            break;
          case "true":
          case "false":
            $("#unlisted_status").find('i').attr("class", icon);
            unlisted = id;
            break;
          case "ad":
          case "award":
          case "kiss":
          case "web":
          case "nonsense":
            $("#categories").find('i').attr("class", icon);
            categories = id;
            break;
          case "text/plain1":
          case "image1":
          case "text/markdown1":
            $("#contentType1").find('i').attr("class", icon);
            contentType = id;
            // handle upload button
            if (id == "image1"){
               $("#imageFile1").attr("style", "display: block");
            } else {
              $("#imageFile1").attr("style", "display: none");

            }
          default:
            $("#contentType").find('i').attr("class", icon);
            contentType = id;
            // handle upload button
            console.log("hererrer")
            if (id == "image"){
               $("#imageFile").attr("style", "display: block");
            } else {
              $("#imageFile").attr("style", "display: none");
            }
        }



    });

        // deal with 2 dropdown lists: visibility and contentType
    $('div.dropdown-content-edit a').click(function(e)
      {
       var id = $(this).attr("id")
       var icon = $(this).find("i").attr("class");

       switch (id) {
          case "text/plain" :
          case "image":
          case "text/markdown":
            $("#contentType").find('i').attr("class", icon);
            contentType = id;
            // handle upload button
            console.log("hererrer")
            if (id == "image"){
               $("#imageFile").attr("style", "display: block");
            } else {
              $("#imageFile").attr("style", "display: none");
            }
        }

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

      form_data.append("type", "post");
      form_data.append("contentType", contentType);
      form_data.append("visibility", visibility);
      form_data.append("title", title);
      form_data.append("unlisted", unlisted);
      form_data.append("description", description);
      form_data.append("categories", categories);
      form_data.append("csrfmiddlewaretoken", csrftoken);

      console.log("description");
      $.ajax({
        url : ".", // the endpoint
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
    });

});

