jQuery(document).ready(function($) {

  $.ajax({
    url : "../public_channel/{{friend.id}}/", // the endpoint
    type : "GET", // http method
    contentType: false,
    processData: false,
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
    },
  });


});
