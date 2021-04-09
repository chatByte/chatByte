'use strict'
var contentType = 'text';
var visibility = 'public';
var description = "";
var title = "";
var form_data = new FormData();
var edit_form_data = new FormData();
var x_server = window.location.origin;

var url = window.location.href;

var new_url = url.split('/');





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


function editButton(title, description) {
  $('body').on('click', 'a.editBtn', function(e) {
    e.preventDefault();

    var content_holder = $(this).closest('.post-detail').find('p')

    content_holder.attr("style", "display: none");
    // var div_content = $('div .form-group-col').html();
    var div_content = $('div .form-group-col').clone();
    var find_element = div_content.find('#title');
    var find_description = div_content.find('#description');
    // console.log(find_element);
    find_element.attr("id", "editTitle");
    find_element.text(title);

    find_description.attr("id", "editDescription");
    find_description.text(description);

    // console.log(find_element);
    var new_div = $(this).closest('.post-detail').find('div .editText')
    new_div.attr("style", "display: block");
    new_div.html(div_content.html());


    // show submit btn, hide edit btn
    $(this).attr("style", "display: none");
    $(this).closest('div .edit').find('.submitBtn').attr("style", "display: block");

  });

}


jQuery(document).ready(function($) {
  const csrftoken = getCookie('csrftoken');

  // like a post
  $('body').on('click', '.like', function(){
    // alert("liked")
    
    var csrftoken = getCookie('csrftoken');

    var post_id = $(this).closest('.post-content').attr('id');

    var data = {type: "like",
                object_type: "post",
                object_id: post_id,
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
                    "Origin": window.location.origin
                },
      data: JSON.stringify(data),
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
          var like_num = $(this).parent('a').text();
          if(!like_num) {
            $(this).text(1);
          } else {
            $(this).text(parseInt(like_num) + 1);
          }
      },
    });

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
          console.log(data); // sanity check
      },
    });

  });
});