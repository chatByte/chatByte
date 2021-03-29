
'use strict'
var url      = window.location.href;
var new_url = url.split('/');
var url_header = "http://"+ new_url[1].toString()  + new_url[2].toString() + '/';
console.log(url_header)

var request_id_list = [];
var inbox_num;
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

//Preloader
var preloader = $('#spinner-wrapper');
$(window).on('load', function() {
    var preloaderFadeOutTime = 500;

    function hidePreloader() {
        preloader.fadeOut(preloaderFadeOutTime);
    }
    hidePreloader();
});

// check if new friend request
function ifFriendRequest(){
  var x_server = window.location.origin
  $.ajax({
    url : url_header + "ifFriendRequest/", // the endpoint
    // header
    headers: {"X-Server": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    type : "GET", // http method
    contentType: false,
    processData: false,
    // handle a successful response
    success : function(data) {
        if (data == undefined) {
          return true
        } else {
          console.log(data); // sanity check
          // request_id_list.includes(data.id) == false
          if ($("#"+data.id).length == 0) {
            $("#myInbox ul").append('<li><a href="" id='+data.id+'>'+data.friend + ' has sent you a friend request!</a><button>Accept</button><button>Reject</button></li>');
            request_id_list.push(data.id);

            var inbox_num = $(".badge").text();
            console.log(inbox_num)
            if(!inbox_num) {
              $(".badge").text(1);
            } else {
              $(".badge").text(parseInt(inbox_num) + 1);
            }
          };
        }


    },
  });
}

jQuery(document).ready(function($) {
  const csrftoken = getCookie('csrftoken');

  // handle follow a person (send friend request)
  $('body').on('click', '.befriend',function(){

    $(this).text("Friend Request Sent");

    console.log($(this).val())
    $.ajax({
      // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
      url:$(this).val(),
      type : "GET", // http method
      // header
      headers: {"X-Server": x_server},
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      contentType: false,
      processData: false,
      dataType: "json",
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
      },
    });
  });

  // handle unfollow a friend
  $('body').on('click', '.unfriend',function(){
    $(this).text("Befriend");
    console.log($(this).val())
    $.ajax({
      // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
      url:$(this).val(),
      type : "GET", // http method
      contentType: false,
      processData: false,
      dataType: "json",
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
      },
    });
  });


  // handle accept of friend request
  $('body').on('click', '.accept', function(){
    var request_id = $(this).parent('li').find('a').attr('id');
    console.log(request_id);
    $(this).parent('li').remove();

    var inbox_num = $(".badge").text();
    if (inbox_num == 1) {
      $(".badge").text('');
    } else {
      $(".badge").text(parseInt(inbox_num) - 1);
    }

    $.ajax({
      // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
      url:url_header + 'author/' + new_url[5].toString() + "/friends/accept/" + request_id + '/',
      type: "GET", // http method
      contentType: false,
      processData: false,
      dataType: "json",
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
      },
    });
  });

  // handle reject of friend request
  $('body').on('click', '.reject', function(){
    var request_id = $(this).parent('li').find('a').attr('id');
    console.log(request_id);
    $(this).parent('li').remove();

    var inbox_num = $(".badge").text();
    if (inbox_num == 1) {
      $(".badge").text('');
    } else {
      $(".badge").text(parseInt(inbox_num) - 1);
    }

    $.ajax({
      // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
      url:url_header + 'author/' + new_url[5].toString() + "/friends/reject/" + request_id + '/',
      // header
      headers: {"X-Server": x_server},
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },
      type: "GET", // http method
      contentType: false,
      processData: false,
      dataType: "json",
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
      },
    });
  });


  // like a post
  $('body').on('click', '.like', function(){
    // alert("liked")
    var like_num = $(this).parent('a').text();
    if(!like_num) {
      $(this).text(1);
    } else {
      $(this).text(parseInt(like_num) + 1);
    }

    var post_id = $(this).closest('.post-content').attr('id');

    var data = {type: "like",
                object: post_id,
                csrfmiddlewaretoken: csrftoken
                // summary:"someone liked someone's post"
                // context:
                }
    // console.log(window.location.origin+'/author/'+ new_url[5].toString() +'/inbox/')
    $.ajax({
      // author/<str:AUTHOR_ID>/inbox/
      type: "POST", // http method
      url:window.location.origin+'/author/'+ new_url[4].toString() +'/inbox/',
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

  setInterval(ifFriendRequest, 5000);

});
