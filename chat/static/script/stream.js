'use strict'
var contentType = 'text/plain';
var visibility = 'public';
var description = "";
var title = "";
var form_data = new FormData();
var edit_form_data = new FormData();
var x_server = window.location.origin;

var url = window.location.href;

var new_url = url.split('/');
var comment_post_id = "";




//Preloader
var preloader = $('#spinner-wrapper');
$(window).on('load', function() {
    var preloaderFadeOutTime = 500;

    function hidePreloader() {
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
});



function search(ID){
  var id = ID;
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

// design for like post
function likePost(post_id, liked) {
  // like a post
  if (liked) return;

  var csrftoken = getCookie('csrftoken');

  // var post_id = $(this).closest('.post-content').attr('id');
  console.log("post id: ", post_id)

  var data = {type: "like",
              object_type: "post",
              object_id: post_id,
              // summary: "likes your post",
              csrfmiddlewaretoken: csrftoken
              // context:
              }
  // console.log(window.location.origin+'/author/'+ new_url[5].toString() +'/inbox/')
  $.ajax({
    // author/<str:AUTHOR_ID>/inbox/
    type: "POST", // http method
    url:window.location.origin+'/author/'+ new_url[4].toString() +'/my_stream/',
    // header
    headers: {"X-Server": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    headers:{
                  "X-CSRFToken": csrftoken,
              },
    data: JSON.stringify(data),
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        var like_num = $(this).parent('a').text();
        if(liked) {
          $(this).text(parseInt(like_num) - 1);
        } else {
          $(this).text(parseInt(like_num) + 1);
        }
        window.location.reload();
    },
  });
}

function likeComment(comment_id, liked) {
  // like a post
  if (liked) return;

  var csrftoken = getCookie('csrftoken');

  // var post_id = $(this).closest('.post-content').attr('id');
  console.log("comment_id : ", comment_id)

  var data = {type: "like",
              object_type: "comment",
              object_id: comment_id,
              // summary: "likes your post",
              csrfmiddlewaretoken: csrftoken
              // summary:"someone liked someone's post"
              // context:
              }
  // console.log(window.location.origin+'/author/'+ new_url[5].toString() +'/inbox/')
  $.ajax({
    // author/<str:AUTHOR_ID>/inbox/
    type: "POST", // http method
    url:window.location.origin+'/author/'+ new_url[4].toString() +'/my_stream/',
    // header
    headers: {"X-Server": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    headers:{
                  "X-CSRFToken": csrftoken,
              },
    data: JSON.stringify(data),
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        var like_num = $(this).parent('a').text();
        if(liked) {
          $(this).text(parseInt(like_num) - 1);
        } else {
          $(this).text(parseInt(like_num) + 1);
        }
        window.location.reload();
    },
  });
}


function reshare(post_id){
  console.log(post_id)
  $.ajax({
    url:"../reshare/",
    type: "POST", // http method
    // header
    headers: {"X-SERVER": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    data: JSON.stringify({
      "post_id": post_id
    }),
    // fields = ['type','id', 'host', 'displayName', 'url', 'github']
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        window.location.reload();
    },
  });
}

jQuery(document).ready(function($) {
  const csrftoken = getCookie('csrftoken');
  console.log(x_server + '/author/' +new_url[4].toString() + '/github/');


  // deal with 2 dropdown lists: visibility and contentType
  $('div.dropdown-content a').click(function(e)
  {
    var id = $(this).attr("id")
    var icon = $(this).find("i").attr("class");
    console.log(icon);
    $("#contentType").find('i').attr("class", icon);
    contentType = id;
    // handle upload button
    if (id == "image"){
      $("#imageFile").attr("style", "display: block");
    } else {
      $("#imageFile").attr("style", "display: none");
    }

  });

  //like a comment
  $('body').on('click', '.comment-like', function(){
    var like_num = $(this).parent('a').text();
    if(!like_num) {
      $(this).text(1);
    } else {
      $(this).text(parseInt(like_num) + 1);
    }

    var comment_id = $(this).closest('.post-comment').attr('id');

    var data = {type: "like",
                object: comment_id,
                csrfmiddlewaretoken: csrftoken,
                // summary:"someone liked someone's post"
                // context:
                }

    $.ajax({
      // author/<str:AUTHOR_ID>/inbox/
      url:window.location.origin+'/author/'+ new_url[4].toString() +'/inbox/',
      type: "POST", // http method
      // header
      headers: {"X-SERVER": x_server},
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
      data: {type: "Like",
                  object: comment_id,
                  csrfmiddlewaretoken: csrftoken,
                  // summary:"someone liked someone's post"
                  // context:
                },
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check\
      },
    });

  });

  // create a new comment
  $('.postBtn').click(function(e){
    console.log("making comment...");
    comment_post_id = $(this).attr('id');
    console.log("current comment post id: ", comment_post_id)
  });

  // create a new comment
  $('.submitComment').click(function(e){
    console.log("here");

    var csrftoken = getCookie('csrftoken');

    var description = document.getElementById("description").value;
    console.log("Comment description: ", description);

    // var post_id = $(this).attr('id');
    console.log("post id: ", comment_post_id)

    var x_server = comment_post_id.split('author/')[0]
    console.log("X-server header: ", x_server);
    var data = {type: "comment",
                comment: description,
                post_id: comment_post_id,
                content_type: contentType
                }
    // console.log(window.location.origin+'/author/'+ new_url[5].toString() +'/inbox/')
    $.ajax({
      // author/<str:AUTHOR_ID>/inbox/
      type: "POST", // http method
      url:window.location.origin+'/author/'+ new_url[4].toString() +'/my_stream/',
      // header
      headers: {"X-Server": x_server},
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      contentType: 'application/json; charset=utf-8',
      dataType: "json",
      headers:{
                    "X-CSRFToken": csrftoken,
                },
      data: JSON.stringify(data),
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
          window.location.reload();
      },
    });
  });
});
