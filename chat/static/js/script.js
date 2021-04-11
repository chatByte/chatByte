'use strict'
var url = window.location.href;

var new_url = url.split('/');
// var url_header = "https://"+ new_url[1].toString()  + new_url[2].toString() + '/';
// on local testing
var url_header = "https://"+ new_url[1].toString()  + new_url[2].toString() + '/';
console.log(url_header);
// var x_server = window.location.origin + '/author/'+new_url[4].toString();
var x_server = window.location.origin +'/';
// var x_server = "http://127.0.0.1:8000/";
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

// check if new friend request
// function ifFriendRequest(){
//   var x_server = window.location.origin
//   $.ajax({
//     url : url_header + "ifFriendRequest/", // the endpoint
//     // header
//     headers: {"X-Server": x_server},
//     beforeSend: function(xhr) {
//       xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//     },
//     type : "GET", // http method
//     contentType: false,
//     processData: false,
//     // handle a successful response
//     success : function(data) {
//         if (data == undefined) {
//           return true
//         } else {
//           // console.log(data); // sanity check
//           // request_id_list.includes(data.id) == false
//           if ($("#"+data.id).length == 0) {
//             // $("#myInbox ul").append('<li><a href="" id='+data.id+'>'+data.friend + ' has sent you a friend request!</a><button>Accept</button><button>Reject</button></li>');
//             // request_id_list.push(data.id);

//             var inbox_num = $(".badge").text();
//             console.log(inbox_num)
//             if(!inbox_num) {
//               $(".badge").text(1);
//             } else {
//               $(".badge").text(parseInt(inbox_num) + 1);
//             }
//           };
//         }
//     },
//   });
// }


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
    // fields = ['type','id', 'host', 'displayName', 'url', 'github']
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
    },
  });

}



// add myself to be others followers
function putFollow(type, id, host, displayName, url, github, foreignId){
  create_following();

  x_server = foreignId.split("author/")[0];


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
        console.log(data); // sanity check
    },
  });
}

// function sendFriendRequest(type, summary, author, object) {


//   console.log("sening Friend Request");
//   $.ajax({
//     // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
//     url:window.location.origin+'/author/'+ new_url[4].toString() +'/inbox/',
//     type : "POST", // http method
//     // header
//     headers: {"X-Server": x_server},
//     beforeSend: function(xhr) {
//       xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//     },
//     contentType: false,
//     processData: false,
//     dataType: "json",
//     data: JSON.stringify({
//       type: 'follow',
//       summary: summary,
//       author: author,
//       object: object,
//     }),
//     // handle a successful response
//     success : function(data) {
//         console.log(data); // sanity check
//     },
//   });
// }

function sendFriendRequest(type, summary, author, object) {
  var foreign_id = object["id"];
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
    // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
    url: window.location.origin +'/author/'+ new_url[4].toString() +'/inbox',
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



// be friend , to send friend request
function be_friend(type, id, host, displayName, url, github) {
    var summary = displayName + " want to be friend with you";



    var actor =
    { type: type,
      id: id,
      host: host,
      displayName: displayName,
      url: url,
      github: github };

    $.ajax({
    //http://127.0.0.1:8000/author/6/my_stream/david/1/
    url:window.location.origin+'/get_user/'+ new_url[6].toString() +"/"+ new_url[7].toString() +'/',
    type:"GET",

    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    },


    success: function(data){
      console.log("---------------------befriend, data");
      console.log(data);
      object = data;
      sendFriendRequest("Follow",summary, actor, object);
    }
  });

}

function accept_or_reject(decision, request_id){
  $.ajax({
    // first author id is who I want to follow
    // second author id is who I am
    // http://127.0.0.1:8000/author/1/my_stream/david/5/



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

function unbefriend(friend_id){
  $.ajax({
    // first author id is who I want to follow
    // second author id is who I am
    // http://127.0.0.1:8000/author/1/my_stream/david/5/



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
    // fields = ['type','id', 'host', 'displayName', 'url', 'github']
    // handle a successful response
    success : function(data) {
        console.log(data); // sanity check
        window.location.reload();
    },
  });
}

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

  // // handle follow a person (send friend request)
  // $('body').on('click', '.befriend',function(){

  //   $(this).text("Friend Request Sent");

  //   console.log($(this).val())
  //   // // views.py
  //   // $.ajax({
  //   //   // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
  //   //   url:$(this).val(),
  //   //   type : "GET", // http method
  //   //   // header
  //   //   headers: {"X-Server": x_server},
  //   //   beforeSend: function(xhr) {
  //   //     xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  //   //   },
  //   //   contentType: false,
  //   //   processData: false,
  //   //   dataType: "json",
  //   //   // handle a successful response
  //   //   success : function(data) {
  //   //       console.log(data); // sanity check
  //   //   },
  //   // });

  //   // api.py
  //   //  fields = ['type','id', 'summary', 'author', 'object']
  //   // first get user info


  //   $.ajax({
  //     url:window.location.origin+'/get_user/'+ new_url[4].toString() +'/',
  //     type:"GET",
  //     success: function(data){
  //       console.log(data);
  //       author = data;

  //       $.ajax({
  //         //http://127.0.0.1:8000/author/6/my_stream/david/1/
  //         url:window.location.origin+'/get_user/'+ new_url[6].toString() +"/"+ new_url[7].toString() +'/',
  //         type:"GET",
  //         success: function(data){
  //           console.log(data);
  //           object = data;
  //           sendFriendRequest(type, id, summary, author, object)
  //         }
  //       });
  //     },
  //   });
  // });

  // handle unfollow a friend
  $('body').on('click', '.unfriend',function(){
    $(this).text("Befriend");
    console.log($(this).val())
    $.ajax({
      // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
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


  // handle accept of friend request
  // $('body').on('click', '.accept', function(){
  //   var request_id = $(this).parent('li').find('a').attr('id');
  //   console.log(request_id);
  //   $(this).parent('li').remove();

  //   var inbox_num = $(".badge").text();
  //   if (inbox_num == 1) {
  //     $(".badge").text('');
  //   } else {
  //     $(".badge").text(parseInt(inbox_num) - 1);
  //   }


    // console.log(url_header + 'author/' + new_url[5].toString() + "/friends/accept/" + request_id + '/')
    // $.ajax({
    //   // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
    //   url:url_header + 'author/' + new_url[5].toString() + "/friends/accept/" + request_id + '/',
    //   type: "GET", // http method
    //   headers: {"X-Server": x_server},
    //   beforeSend: function(xhr) {
    //     xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    //   },
    //   contentType: false,
    //   processData: false,
    //   dataType: "json",
    //   // handle a successful response
    //   success : function(data) {
    //       console.log(data); // sanity check
    //   },
    // });
  });


  // // handle reject of friend request
  // $('body').on('click', '.reject', function(){
  //   var request_id = $(this).parent('li').find('a').attr('id');
  //   console.log(request_id);
  //   $(this).parent('li').remove();

  //   var inbox_num = $(".badge").text();
  //   if (inbox_num == 1) {
  //     $(".badge").text('');
  //   } else {
  //     $(".badge").text(parseInt(inbox_num) - 1);
  //   }

  //   $.ajax({
  //     // url : url_header + "author/" +  new_url[4].toString() +"/friends/add/{{myId}}/", // the endpoint
  //     url:url_header + 'author/' + new_url[5].toString() + "/friends/reject/" + request_id + '/',
  //     // header
  //     headers: {"X-Server": x_server},
  //     beforeSend: function(xhr) {
  //       xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  //     },
  //     type: "GET", // http method
  //     contentType: false,
  //     processData: false,
  //     dataType: "json",
  //     // handle a successful response
  //     success : function(data) {
  //         console.log(data); // sanity check
  //     },
  //   });
  // });


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


  // $('body').on('click', '#followBtn', function(){

  //   // $('#following').attr("style", "display: block");
  //   $(this).parent('a').html("<h4>Following</h4>");

  //   // $.ajax({
  //   //   url:window.location.origin+'/get_user',
  //   //   type:"GET",
  //   //   success: function(data){
  //   //     console.log(data)
  //   //     var id = data.id;
  //   //     var host = data.host;
  //   //     var type = data.type;
  //   //     var displayName = data.displayName;
  //   //     var github = data.github;
  //   //   }
  //   // });


  //   console.log("clicked follow button")
  //   console.log(window.location.origin+'/author/'+ new_url[4].toString() +'/followers/'+new_url[6].toString())

  //   // //can use Jinjia {{}}
  //   // var id = {{cur_author.id}};
  //   // var host = {{cur_author.host}};
  //   // var type = {{cur_author.type}};
  //   // var displayName = {{cur_author.displayName}};
  //   // var github = {{cur_author.github}};

  //   // console.log("Jinjia: ", id, host, type, displayName, github )


  //   var test = "{{cur_author}}";
  //   console.log("Jinjia: ", test)

  // });

  // setInterval(ifFriendRequest, 5000);

// });
