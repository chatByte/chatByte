'use strict'
var url = window.location.href;

var new_url = url.split('/');
var url_header = "https://"+ new_url[1].toString()  + new_url[2].toString() + '/';
console.log(url_header);
var x_server = window.location.origin +'/';
var request_id_list = [];
var inbox_num;

var author;
var object;


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


// create a following, add foreigner to be my followings
function create_following() {
    var cur_author_id = new_url[4].toString();
    var foreign_id = new_url[7].toString();
    console.log(cur_author_id);
    console.log(foreign_id);

    $.ajax({
    // "author/<str:AUTHOR_ID>/following/<str:FOREIGN_AUTHOR_ID>/"
    url:window.location.origin+'/author/'+ cur_author_id +'/following/' + new_url[6] + "/" + foreign_id + "/",
    type: "POST", // http method
    // header
    headers: {"X-SERVER": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    data: JSON.stringify({
    }),
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
    },
  });

}



// add myself to be others followers
function putFollow(type, id, host, displayName, url, github, foreignId){
  create_following();

  console.log("After create following...");
  x_server = foreignId.split("author/")[0];
  console.log("x-server", x_server);

  $.ajax({
    // first author id is who I want to follow
    // second author id is who I am
    // http://127.0.0.1:8000/author/1/my_stream/david/5/
    url:window.location.origin+'/author/'+ new_url[7].toString() +'/followers/'+new_url[4].toString(),
    type: "PUT", // http method
    // header
    headers: {"X-SERVER": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    data: JSON.stringify({
      type: type,
      id: id,
      host: host,
      displayName: displayName,
      url: url,
      github: github

    }),
    // fields = ['type','id', 'host', 'displayName', 'url', 'github']
    // handle a successful response
    success : function(data) {
      console.log("Successfully put as follower")
      console.log(data); // sanity check
    },
  });
}

// send friend request to inbox, used in remote connection
function sendFriendRequest(type, summary, author, object) {
  var foreign_id = object["id"];
  var just_id = foreign_id.split('author/')[1];
  var fi = foreign_id.split("/");
  var x_server_header = fi[0]+"//"+fi[2]+"/";
  console.log("object author id: ", foreign_id);
  console.log("x_server_header: ", x_server_header);

  var data = {
    'type': type,
    'summary': summary,
    'actor': author,
    'object': object
  }
  console.log("Data to be sent: ", JSON.stringify(data))

  console.log("sending Friend Request");
  $.ajax({
    url: window.location.origin +'/author/'+ just_id +'/inbox',
    type : 'POST', // http method
    contentType: "application/json",
    processData: false,
    dataType: 'json',
    data: JSON.stringify(data),
    // header
    headers: {"X-Server": x_server_header},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      console.log("author, obj");
      console.log(author);
      console.log(object);
    },

    // handle a successful response
    success : function(data) {
        // sanity check
        console.log(data);
    },
  });
}



// add friend and save user request, used in local server
function be_friend(type, id, host, displayName, url, github, foreignId) {
    var summary = displayName + " want to be friend with you";

    var actor =
    { type: type,
      id: id,
      host: host,
      displayName: displayName,
      url: url,
      github: github };

    $.ajax({
      url:window.location.origin+'/get_user/'+ new_url[6].toString() +"/"+ new_url[7].toString() +'/',
      type:"GET",

      // header
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
      },

      success: function(data){
        console.log("---------------------befriend, data");
        console.log(data);
        object = data;
        putFollow(type, id, host, displayName, url, github, foreignId);
        sendFriendRequest("Follow",summary, actor, object);
      }
    });

}


// when user is present with a friend request,
// they may chose either to accept - add the actor to their friend;
// or reject - do not add the actor to their friend
// This is not requested but we feel it makes more sense to having this function
function accept_or_reject(decision, request_id){
  $.ajax({
    url:"../makefriend/",
    type: "POST", // http method
    // header
    headers: {"X-SERVER": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    data: JSON.stringify({
      "decision": decision,
      "request_id": request_id
    }),
    // fields = ['type','id', 'host', 'displayName', 'url', 'github']
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        window.location.reload();
    },
  });
}


// unfriend an existing friend
function unbefriend(friend_id){
  $.ajax({
    url:"../unbefriend/",
    type: "POST", // http method
    // header
    headers: {"X-SERVER": x_server},
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },
    contentType: 'application/json; charset=utf-8',
    dataType: "json",
    data: JSON.stringify({
      "friend_id": friend_id
    }),
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        window.location.reload();
    },
  });
}

// reshare a post
function reshare(post_id){
  console.log(post_id)
  $.ajax({
    url:"../../../reshare/",
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

  // handle unfollow a friend
  $('body').on('click', '.unfriend',function(){
    $(this).text("Befriend");
    console.log($(this).val())
    $.ajax({
      url:$(this).val(),
      type : "GET", // http method
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

  // handle like a post
  $('body').on('click', '.like', function(){
    // get like num and increase by 1
    var like_num = $(this).parent('a').text();
    if(!like_num) {
      $(this).text(1);
    } else {
      $(this).text(parseInt(like_num) + 1);
    }

    var post_id = $(this).closest('.post-content').attr('id');

    var data = {type: "like",
                object: post_id,
                csrfmiddlewaretoken: csrftoken,
                }
    $.ajax({
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


});
