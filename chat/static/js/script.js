
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

<<<<<<< HEAD
// jQuery(document).ready(function($) {
//
//     //Incremental Coutner
//     if ($.isFunction($.fn.incrementalCounter))
//         $("#incremental-counter").incrementalCounter();
//
//     //For Trigering CSS3 Animations on Scrolling
//     if ($.isFunction($.fn.appear))
//         $(".slideDown, .slideUp").appear();
//
//     $(".slideDown, .slideUp").on('appear', function(event, $all_appeared_elements) {
//         $($all_appeared_elements).addClass('appear');
//     });
//
//     //For Header Appearing in Homepage on Scrolling
//     var lazy = $('#header.lazy-load')
//
//     $(window).on('scroll', function() {
//         if ($(this).scrollTop() > 200) {
//             lazy.addClass('visible');
//         } else {
//             lazy.removeClass('visible');
//         }
//     });
//
//     //Initiate Scroll Styling
//     if ($.isFunction($.fn.scrollbar))
//         $('.scrollbar-wrapper').scrollbar();
//
//     if ($.isFunction($.fn.masonry)) {
//
//         // fix masonry layout for chrome due to video elements were loaded after masonry layout population
//         // we are refreshing masonry layout after all video metadata are fetched.
//         var vElem = $('.img-wrapper video');
//         var videoCount = vElem.length;
//         var vLoaded = 0;
//
//         vElem.each(function(index, elem) {
//
//             //console.log(elem, elem.readyState);
//
//             if (elem.readyState) {
//                 vLoaded++;
//
//                 if (count == vLoaded) {
//                     $('.js-masonry').masonry('layout');
//                 }
//
//                 return;
//             }
//
//             $(elem).on('loadedmetadata', function() {
//                 vLoaded++;
//                 //console.log('vLoaded',vLoaded, this);
//                 if (videoCount == vLoaded) {
//                     $('.js-masonry').masonry('layout');
//                 }
//             })
//         });
//
//
//         // fix masonry layout for chrome due to image elements were loaded after masonry layout population
//         // we are refreshing masonry layout after all images are fetched.
//         var $mElement = $('.img-wrapper img');
//         var count = $mElement.length;
//         var loaded = 0;
//
//         $mElement.each(function(index, elem) {
//
//             if (elem.complete) {
//                 loaded++;
//
//                 if (count == loaded) {
//                     $('.js-masonry').masonry('layout');
//                 }
//
//                 return;
//             }
//
//             $(elem).on('load', function() {
//                 loaded++;
//                 if (count == loaded) {
//                     $('.js-masonry').masonry('layout');
//                 }
//             })
//         });
//
//     } // end of `if masonry` checking
//
//
//     //Fire Scroll and Resize Event
//     $(window).trigger('scroll');
//     $(window).trigger('resize');
// });
//
// /**
//  * function for attaching sticky feature
//  **/
//
// function attachSticky() {
//     // Sticky Chat Block
//     $('#chat-block').stick_in_parent({
//         parent: '#page-contents',
//         offset_top: 70
//     });
//
//     // Sticky Right Sidebar
//     $('#sticky-sidebar').stick_in_parent({
//         parent: '#page-contents',
//         offset_top: 70
//     });
//
// }
//
// // Disable Sticky Feature in Mobile
// $(window).on("resize", function() {
//
//     if ($.isFunction($.fn.stick_in_parent)) {
//         // Check if Screen wWdth is Less Than or Equal to 992px, Disable Sticky Feature
//         if ($(this).width() <= 992) {
//             $('#chat-block').trigger('sticky_kit:detach');
//             $('#sticky-sidebar').trigger('sticky_kit:detach');
//
//             return;
//         } else {
//
//             // Enabling Sticky Feature for Width Greater than 992px
//             attachSticky();
//         }
//
//         // Firing Sticky Recalculate on Screen Resize
//         return function(e) {
//             return $(document.body).trigger("sticky_kit:recalc");
//         };
//     }
// });
//
// // Fuction for map initialization
// function initMap() {
//   var uluru = {lat: 12.927923, lng: 77.627108};
//   var map = new google.maps.Map(document.getElementById('map'), {
//     zoom: 15,
//     center: uluru,
//     zoomControl: true,
//     scaleControl: false,
//     scrollwheel: false,
//     disableDoubleClickZoom: true
//   });
//
//   var marker = new google.maps.Marker({
//     position: uluru,
//     map: map
//   });
// }
=======

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
>>>>>>> yao
