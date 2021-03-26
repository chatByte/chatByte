
'use strict'


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
    url : "if_friend_request/", // the endpoint
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


  setInterval(ifFriendRequest, 5000);

}
