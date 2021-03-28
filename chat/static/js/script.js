
'use strict'
var url      = window.location.href;
var new_url = url.split('/');
var url_header = "http://"+ new_url[1].toString()  + new_url[2].toString() + '/chat/';
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


function ifFriendRequest(){
  $.ajax({
    url : url_header + "ifFriendRequest/", // the endpoint
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

  $('body').on('click', '.follow',function(){

    $(this).text("Friend Request Sent");

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

  $('body').on('click', '.unfollow',function(){

    $(this).text("Follow");

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
      header: {'origin': window.location.origin},
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

  setInterval(ifFriendRequest, 5000);

});
