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


$( document ).ready(function() {
  // deal with edit button
  // show textarea and hide p
  $('body').on('click', 'a.editBtn', function(e) {
    e.preventDefault();

    var content_holder = $(this).closest('.post-detail').find('p')


    $(this).closest('.post-detail').find('.edit-block').attr("style", "display: block");
    content_holder.attr("style", "display: none");
  });

})
