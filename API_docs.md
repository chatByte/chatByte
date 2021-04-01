# Social Distribution Api Documentation
### Request Headers
    - Local Request: {
        Authorization: CSRF Token,
        X-server: where is it coming from.
    }
    - Remote Request: {
        Authorization: Basic <Base64 Encoded username:password>,
        Origin: <Host from which the request originates>,
        X-Request-User: <Full URL id of the author making the request>
    }
    
### **Author Profile API**
URL: ://service/author/{AUTHOR_ID}/
GET: retrieve their profile
POST: update profile

#### `Author Object format`

```
{ 
"type": "author",
 	"id": "https://chatbyte.herokuapp.com/author/1", 
"host": null, 
"displayName": "test", 
"url": null, 
"github": null
}

```

#### `GET`
<i>retrieve their profile</i>
```
URL: ://service/author/{AUTHOR_ID}/
```
Response:
```
Response (200):
{
    "type":"author",
    "id":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "host":"http://127.0.0.1:8000/",
    "displayName":"Lara Croft",
    "url":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "github": "http://github.com/laracroft"
}
```

#### `POST`
<i>update profile</i>
```
URL: ://service/author/{AUTHOR_ID}/
```
Body of Request:
```
{
    "type":"author",
    "id":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "host":"http://127.0.0.1:8000/",
    "displayName":"Lara Croft",
    "url":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "github": "http://github.com/laracroft"
}
```
Response:
```
Response (200):
{
    "type":"author",
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "host":"http://127.0.0.1:5454/",
    "displayName":"Lara Croft",
    "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
    "github": "http://github.com/laracroft"
}
```

### **Follower API**
### `GET`
<i>get a list of authors who are their followers</i>
```
URL: ://service/author/{AUTHOR_ID}/followers
```
Response:
```
Response (200):
{
    "type": "followers",      
    "items":[
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        },
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara Croft",
            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "github": "http://github.com/laracroft"
        }
    ]
}
```

### `GET`
<i>check if follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
Response:
```
Response (200):
{
"detail":'true';
}
```
or
```
Response (200):
{
"detail":'false';
}
```

### `PUT`
<i>Add a follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
Response:
```
Response (200):
{
"followee":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
"follower_url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
}

```

### `DELETE`
<i>remove a follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
Response:
```
Response (200):
<None>
```

### **Friend API**
### `GET`
<i>get all friends of author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```
Response:
```
Response (200):
{
    "type": "friends",      
    "items":[
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        },
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara Croft",
            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "github": "http://github.com/laracroft"
        }
    ]
}
```

### `POST`
<i>add a friend to author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```
Body of Request:
```
{
"url":"http://127.0.0.1:5454/author/8de17f29c12e8f97bcbbd34cc908f1baba40658e",
}
```
Response:
```
Response (200):
<None>
```

### `DELETE`
<i>delete a friend from author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```
Body of Request:
```
{
"url":"http://127.0.0.1:5454/author/8de17f29c12e8f97bcbbd34cc908f1baba40658e",
}
```
Response:
```
Response (200):
<None>
```

### `GET`
<i>get all authors has the author as friend</i>
```
URL: ://service/author/asFriend/<query: url=<url of the author>>
```
Response:
```
Response (200):
{
    "type": "asFriend",      
    "items":[
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Greg Johnson",
            "github": "http://github.com/gjohnson"
        },
        {
            "type":"author",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara Croft",
            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "github": "http://github.com/laracroft"
        }
    ]
}
```

    
### **Comments API**
#### `Comment Object format`
```
{
    "type":"comment",
	"author":{
              "type":"author",
	            # ID of the Author (UUID)
              "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
              # url to the authors information
              "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
	        "host":"http://127.0.0.1:5454/",
	       "displayName":"Greg Johnson",
	       # HATEOS url for Github API
	       "github": "http://github.com/gjohnson"
         }
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    # ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    # ID of the Comment (UUID)
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
}
```
#### `GET`
<i>Get comments for a Post</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/comments
```
- Supports Pagination through **query parameters**
    - page -> Default value is set to 1 if not provided
    - size -> Default value is set to 5 if not provided
```
Response (200):
{
    count: 0, # Number of comments for post
    comments: [List of Comment Objects],
    next: url to the next page if exists else "",
    prev: url to the prev page if exists, else "",
}
```
#### `POST`
<i>Create Comment on a Post</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/comments
```
Body of Request:
```
{
    content: "some content",
    contentType: "some content type"
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)



### **Likes API**
#### `Like Object format`
```
{
     "@context": "https://www.w3.org/ns/activitystreams",
     "summary": "Lara Croft Likes your post",         
     "type": "Like",
     "author":{
         "type":"author",
          "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "host":"http://127.0.0.1:5454/",
         "displayName":"Lara Croft",
         "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "github":"http://github.com/laracroft"
     },
     "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}
```
#### `GET`
<i>Get Likes for a Post</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/likes
```
```
Response (200):
[
    List of Like Objects
]
```
<i>Get Likes for a Comment</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
```
```
Response (200):
[
    List of Like Objects
]
```
#### `POST`
<i>Create a Like for either a Post or a Comment</i>
<br>
<i>Side Effect: Sends To Inbox</i>
```
://service/author/{AUTHOR_ID}/likes
```
```
Request Body:
Comment Object || Post Object

Depending on which is sent, a corresponding like will be created.
```

### **Liked API**
#### `Liked Object format`
```
{
    "type":"liked",
    "items":[
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "summary": "Lara Croft Likes your post",         
            "type": "Like",
            "author":{
                "type":"author",
                   "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Lara Croft",
                "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                "github":"http://github.com/laracroft"
            },
            "object":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
        }
    ]
}
```
#### `GET`
<i>Get Liked for an author</i>
```
://service/author/{AUTHOR_ID}/liked
```

### **Post API**
#### `Post Object format`

```
{
    # total number of posts, customized field
    "count": 2,
    # requirement json object start from here
    "posts": [
        {
            "type": "post",
            "title": "2222",
            "id": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b/posts/2222",
            "source": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b/posts/2222",
            "origin": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b/posts/2222",
            "description": "22222",
            "contentType": "text/plain",
            "content": "22222",
            "author": {
                "type": "author",
                "id": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b",
                "host": "http://localhost:8000/",
                "displayName": "123",
                "url": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b",
                "github": "https://github.com/"
            },
            "categories": "[]",
            "count": 0,
            "size": 1,

	# Asked Zoe, we are allowed to replace comment into unique name
            "comment_url": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b/posts/2222/comments",
            "comments": [],
            "published": "2021-03-22T08:33:09.910Z",
            "visibility": "public",
            "unlisted": false
        }
    ],
    # link to next page, customized field
    "next": "http://localhost:8000/author/d63554f7-6d78-45b5-81c5-5b954b59320b/posts/?page=2&size=1",
    #link to prev page, customized field
    "prev": ""
}

```
#### `GET`

<i>Get Post Using PostId</i>

```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
```

Response (200):
```
post object from spec
{
    "type":"post",
    # title of a post
    "title":"A post title about a post about web dev",
    # id of the post
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
    # where did you get this post from?
    "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
    # where is it actually from
    "origin":"http://whereitcamefrom.com/posts/zzzzz",
    # a brief description of the post
    "description":"This post discusses stuff -- brief",
    # The content type of the post
    # assume either
    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64 # this is an embedded png -- images are POSTS. So you might have a user make 2 posts if a post includes an image!
    # image/jpeg;base64 # this is an embedded jpeg
    # for HTML you will want to strip tags before displaying
    "contentType":"text/plain",
    "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
    # the author has an ID where by authors can be disambiguated
    "author":{
            "type":"author",
            # ID of the Author
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            # the home host of the author
            "host":"http://127.0.0.1:5454/",
            # the display name of the author
            "displayName":"Lara Croft",
            # url to the authors profile
            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            # HATEOS url for Github API
            "github": "http://github.com/laracroft"
    },
    # categories this post fits into (a list of strings
    "categories":["web","tutorial"],
    # comments about the post
    # return a maximum number of comments
    # total number of comments for this post
    "count": 1023,
    # page size
    "size": 50,
    # the first page of comments
    "comment_url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments"
    # You should return ~ 5 comments per post.
    # should be sorted newest(first) to oldest(last)
    "comments":[
        {
             "type":"comment",
             "author":{
                "type":"author",
                # ID of the Author (UUID)
                "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                # url to the authors information
                "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
                "host":"http://127.0.0.1:5454/",
                "displayName":"Greg Johnson",
                # HATEOS url for Github API
                "github": "http://github.com/gjohnson"
             },
             "comment":"Sick Olde English",
             "contentType":"text/markdown",
             # ISO 8601 TIMESTAMP
             "published":"2015-03-09T13:07:04+00:00",
             # ID of the Comment (UUID)
             "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
        }
    ]
    # ISO 8601 TIMESTAMP
    "published":"2015-03-09T13:07:04+00:00",
    # visibility ["PUBLIC","FRIENDS"]
    "visibility":"PUBLIC",
    # for visibility PUBLIC means it is open to the wild web
    # FRIENDS means if we're direct friends I can see the post
    # FRIENDS should've already been sent the post so they don't need this
    "unlisted":false
    # unlisted means it is public if you know the post name -- use this for images, it's so images don't show up in timelines
}

```

<i>Get Post Using AuthorId</i>

```
://service/author/{AUTHOR_ID}/posts/
```
Response (200):
```
{
    count: 0, # Number of comments for post
    posts: [List of Post Objects],
    next: url to the next page if exists else "",
    prev: url to the prev page if exists, else "",
}
```
- Supports Pagination through **query parameters**
    - page -> Default value is set to 1 if not provided
    - size -> Default value is set to 5 if not provided


<i>Get Stream Using AuthorId</i>

```
://service/author/{AUTHOR_ID}/stream
```

Response (200):
```
{
    count: 0, # Number of comments for post
    posts: [List of Post Objects],
    next: url to the next page if exists else "",
    prev: url to the prev page if exists, else "",
}
```
- Supports Pagination through **query parameters**
    - page -> Default value is set to 1 if not provided
    - size -> Default value is set to 5 if not provided


#### `POST`
<i>Create A Post By AuthorId</i>
<br>
<i>Side Effect: Sends To Friend Inbox</i>

```
://service/author/{AUTHOR_ID}/posts/
```

Body of Request:
```
{
    title: "title",
    description: "description",
    content: "some content",
    contentType: "some content type",
    visibility: "public",
    categories: [],
    author_id: "1d698d25ff008f7538453c120f581471",
    unlisted: false
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)
Allowed visibility: (public, friend, private)

<i>Edit A Post By AuthorId</i>

```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
```

Body of Request:
```
{
    title: "title",
    description: "description",
    content: "some content",
    contentType: "some content type",
    visibility: "public",
    categories: [],
    author_id: "1d698d25ff008f7538453c120f581471",
    unlisted: false
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)
Allowed visibility: (public, friend, private)


#### `DELETE`
<i>Delete A Post By PostId</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
```

#### `PUT`
<i>Create A Post By PostId</i>
<br>
<i>Side Effect: Sends To Friend Inbox, Erase Own Post With Same PostId</i>
Body of Request:
```
{
    title: "title",
    description: "description",
    content: "some content",
    contentType: "some content type",
    visibility: "public",
    categories: [],
    author_id: "1d698d25ff008f7538453c120f581471",
    unlisted: false
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)
Allowed visibility: (public, friend, private)


### **Inbox API**

#### `inbox Object format`
```
{
    "type":"inbox",
    "author":"http://127.0.0.1:5454/author/c1e3db8ccea4541a0f3d7e5c75feb3fb",
    "items":[
        {
            "type":"post",
            "title":"DID YOU READ MY POST YET?",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/999999983dda1e11db47671c4a3bbd9e"
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"Whatever",
            "contentType":"text/plain",
            "content":"Are you even reading my posts Arjun?",
            "author":{
                  "type":"author",
            	"id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            	"host":"http://127.0.0.1:5454/",
            	"displayName":"Lara Croft",
            	"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            	"github": "http://github.com/laracroft"
            },
            "categories":["web","tutorial"],
            "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments"
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"FRIENDS",
            "unlisted":false
        }
    ]
}
```
#### `GET`

<i>Get all inbox for author using author_id</i>

```
://service/author/<str:author_id>/inbox
```

```
Response (200):
{
    "type":"inbox",
    "author":"http://127.0.0.1:5454/author/c1e3db8ccea4541a0f3d7e5c75feb3fb",
    "items":[
        A list of all inbox items for author
    ]
}
```

#### `POST`

<i>Create a inbox obejct for author using author_id</i>

```
://service/author/<str:author_id>/inbox
```

Body of Request (follow inbox):

```
{
    "type": "Follow",      
    "summary":"Greg wants to follow Lara",
    "actor":{
        "type":"author",
        "id":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
        "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Greg Johnson",
        "github": "http://github.com/gjohnson"
    },
    "object":{
        "type":"author",
        "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Lara Croft",
        "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft"
    }
}
```

Body of Request (like inbox):

```
{
    "type":"Like",
            "@context":"",
            "summary":"Ankush Sharma Likes your post",
            "author":{
                "type":"author",
                "id":"http://localhost:8000/author/ecc154e4-eb48-4282-b721-bad9d56ada82",
                "host":"http://localhost:8000/",
                "displayName":"Ankush Sharma",
                "url":"http://localhost:8000/author/ecc154e4-eb48-4282-b721-bad9d56ada82",
                "github":"https://github.com/AnkushSharma2698"
            },
            "object":"http://localhost:8000/author/ecc154e4-eb48-4282-b721-bad9d56ada82/posts/3c11a77e-27cf-47af-8c27-4ff4b97c8cc1"

    
}
```

Body of Request (post inbox):

```
{
    "type":"post",
            "title":"A Friendly post title about a post about web dev",
            "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
            "source":"http://lastplaceigotthisfrom.com/posts/yyyyy",
            "origin":"http://whereitcamefrom.com/posts/zzzzz",
            "description":"This post discusses stuff -- brief",
            "contentType":"text/plain",
            "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
            "author":{
                  "type":"author",
            	"id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            	"host":"http://127.0.0.1:5454/",
            	"displayName":"Lara Croft",
            	"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            	"github": "http://github.com/laracroft"
            },
            "categories":["web","tutorial"],
            "comments":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
            "published":"2015-03-09T13:07:04+00:00",
            "visibility":"FRIENDS",
            "unlisted":false

    
}
```

#### `DELETE`
<i>Delete all inbox for author using author_id</i>

```
://service/author/<str:author_id>/inbox
```

<i>Delete a single inbox for author using author_id and item_id</i>

```
://service/author/<str:author_id>/inbox/<str:item_id>
```
