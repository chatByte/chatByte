
'use strict'
var url      = window.location.href;
var new_url = url.split('/');
var url_header = "http://"+ new_url[1].toString()  + new_url[2].toString() + '/chat/';
console.log(url_header)
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
        console.log(data); // sanity check
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
      // handle a successful response
      success : function(data) {
          console.log(data); // sanity check
      },
    });
  })
  setInterval(ifFriendRequest, 5000);

});
