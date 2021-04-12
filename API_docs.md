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
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/
GET: retrieve their profile
POST: update profile
```
#### `Author Object format` 
<i>retrieve their profile</i>
```
URL:https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/
GET: response(200) 
retrieve user profile
POST: response(200)
update user profile (with pagination)
```
### `GET`
```
{
    "type": "author",
    "id": "https://app-chatbyte.herokuapp.com/author/1",
    "host": "https://app-chatbyte.herokuapp.com/",
    "displayName": "test",
    "url": "https://app-chatbyte.herokuapp.com/author/1",
    "github": "https://app-chatbyte.herokuapp.com/author/1"
}

```
### `POST`
<i>response is the new object</i>
```
{
    "type": "author",
    "id": "https://app-chatbyte.herokuapp.com/author/1",
    "host": "https://app-chatbyte.herokuapp.com/",
    "displayName": "test123",
    "url": "https://app-chatbyte.herokuapp.com/author/1",
    "github": "https://app-chatbyte.herokuapp.com/author/1"
}

```

### **Stream API**
### `GET`
<i>GET USER Stream with Pagination</i>
```
URL: https://app-chatbyte.herokuapp.com/author/<str:AUTHOR_ID>/stream/
```
```
{
    "count": 8,
    "next": "",
    "previous": "",
    "posts": [
        {
            "type": "post",
            "id": "https://app-chatbyte.herokuapp.com/author/1/posts/b2e513ae-ab58-446c-a930-64bd17674447",
            "title": "gugu",
            "source": "https://app-chatbyte.herokuapp.com/author/1",
            "origin": "https://app-chatbyte.herokuapp.com/",
            "description": "gugu",
            "contentType": "text",
            "content": "gugu",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://app-chatbyte.herokuapp.com/author/1/posts/b2e513ae-ab58-446c-a930-64bd17674447/comments/",
            "comments": [],
            "published": "2021-04-01T09:57:38.555123Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/92e9035c-8dc6-446e-be02-da68b86fbee5",
            "title": "gaga",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "gaga",
            "contentType": "text",
            "content": "gaga",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/92e9035c-8dc6-446e-be02-da68b86fbee5/comments/",
            "comments": [],
            "published": "2021-04-01T09:58:00.546001Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://app-chatbyte.herokuapp.com/author/1/posts/767fcb2d-bfce-46c8-a269-990b654b1e71",
            "title": "claire",
            "source": "https://app-chatbyte.herokuapp.com/author/1",
            "origin": "https://app-chatbyte.herokuapp.com/",
            "description": "claire",
            "contentType": "text",
            "content": "claire",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://app-chatbyte.herokuapp.com/author/1/posts/767fcb2d-bfce-46c8-a269-990b654b1e71/comments/",
            "comments": [],
            "published": "2021-04-01T18:10:15.214994Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/9737bb60-cac1-4600-9e04-8abd7f5aea31",
            "title": "yao",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "yao",
            "contentType": "text",
            "content": "yao",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/9737bb60-cac1-4600-9e04-8abd7f5aea31/comments/",
            "comments": [],
            "published": "2021-04-01T18:10:38.835281Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70",
            "title": "ttoo",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "too",
            "contentType": "text",
            "content": "too",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70/comments/",
            "comments": [],
            "published": "2021-04-01T09:30:12.393119Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://app-chatbyte.herokuapp.com/author/7/posts/122ad56c-c153-4f60-9fa4-450c258df40e",
            "title": "test",
            "source": "https://app-chatbyte.herokuapp.com/author/7",
            "origin": "https://app-chatbyte.herokuapp.com/",
            "description": "test",
            "contentType": "text",
            "content": "test",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/7",
                "host": null,
                "displayName": "choo",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "",
            "comments": [],
            "published": "2021-04-01T09:37:19.452013Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://app-chatbyte.herokuapp.com/author/7/posts/3aacce7e-407c-4605-8f80-7b1b0a8de08f",
            "title": "choo",
            "source": "https://app-chatbyte.herokuapp.com/author/7",
            "origin": "https://app-chatbyte.herokuapp.com/",
            "description": "choo",
            "contentType": "text",
            "content": "choo",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/7",
                "host": null,
                "displayName": "choo",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "",
            "comments": [],
            "published": "2021-04-01T09:37:43.806644Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://app-chatbyte.herokuapp.com/author/1/posts/0beae2cc-c43d-44ed-928c-e774f5cca749",
            "title": "test",
            "source": "https://app-chatbyte.herokuapp.com/author/1",
            "origin": "https://app-chatbyte.herokuapp.com/",
            "description": "test",
            "contentType": "text",
            "content": "test",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "",
            "comments": [],
            "published": "2021-04-01T09:27:06.948879Z",
            "visibility": "public",
            "unlisted": "false"
        }
    ]
}
```
### **Inbox API**
<i>GET USER notifications in Inbox</i>
```
URL: https://app-chatbyte.herokuapp.com/author/<str:AUTHOR_ID>/inbox/
```
### `GET`

```
{
    "type": "inbox",
    "author": "1",
    "items": [
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70",
            "title": "ttoo",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "too",
            "contentType": "text",
            "content": "too",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70/comments/",
            "comments": [],
            "published": "2021-04-01T09:30:12.393119Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/92e9035c-8dc6-446e-be02-da68b86fbee5",
            "title": "gaga",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "gaga",
            "contentType": "text",
            "content": "gaga",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/92e9035c-8dc6-446e-be02-da68b86fbee5/comments/",
            "comments": [],
            "published": "2021-04-01T09:58:00.546001Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/9737bb60-cac1-4600-9e04-8abd7f5aea31",
            "title": "yao",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "yao",
            "contentType": "text",
            "content": "yao",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/9737bb60-cac1-4600-9e04-8abd7f5aea31/comments/",
            "comments": [],
            "published": "2021-04-01T18:10:38.835281Z",
            "visibility": "public",
            "unlisted": "false"
        },
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/ad35e5e5-cb9d-49e6-a412-e938168ea22a",
            "title": "wow",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "wow",
            "contentType": "text",
            "content": "wow",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/ad35e5e5-cb9d-49e6-a412-e938168ea22a/comments/",
            "comments": [],
            "published": "2021-04-01T09:30:36.174855Z",
            "visibility": "friend",
            "unlisted": "false"
        }
    ]
}
```
### `DELETE`
```
{
    "type": "inbox",
    "author": "1",
    "items": []
}
```
### `POST`

```
POST a post: Response (200)
{
    "type": "inbox",
    "author": "1",
    "items": [
        {
            "type": "post",
            "id": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70abc",
            "title": "ttoo",
            "source": "https://chatbyte.herokuapp.com/author/1",
            "origin": "https://chatbyte.herokuapp.com/",
            "description": "too",
            "contentType": "text",
            "content": "too",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "categories": [
                "text/plain"
            ],
            "count": 0,
            "size": 0,
            "comment_url": "https://chatbyte.herokuapp.com/author/1/posts/5e69d182-2ba3-4093-8633-adbbb1042d70/comments/",
            "comments": [],
            "published": "2021-04-01T09:30:12.393119Z",
            "visibility": "public",
            "unlisted": "false"
        }
    ]
}
```

```
POST a friend Request: Response(200)
Request Body:
{
    "type": "Follow",
    "summary": "Greg wants to follow Lara",
    "actor": {
        "type": "author",
        "id": "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
        "url": "http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Greg Johnson",
        "github": "http://github.com/gjohnson"
    },
    "object": {
        "type": "author",
        "id": "https://app-chatbyte.herokuapp.com/author/1",
        "host": "http://127.0.0.1:5454/",
        "displayName": "Lara Croft",
        "url": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft"
    }
}
```

```
POST a Likes Request: Response(200)
Request Body:
{
     "@context": "https://www.w3.org/ns/activitystreams",
     "summary": "Lara Croft Likes your post",         
     "type": "Like",
     "author": {
         "type":"author",
          "id":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "host":"http://127.0.0.1:8000/",
         "displayName":"Lara Croft",
         "url":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "github":"http://github.com/laracroft"
     },
     "object":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}
```


### ALL POSTS API

#### `GET`
<i>Get all Posts from our server( to other servers), since we are family </i>

```
URL https://app-chatbyte.herokuapp.com/all_posts/
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








### **Post API**
#### `Post Object format`

```
{
    count: 0, # Number of comments for post
    posts: [List of Post Objects],
    next: url to the next page if exists else "",
    prev: url to the prev page if exists, else "",
}
```
#### `GET`

<i>Get Post Using PostId</i>

```
URL:https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts/{POST_ID}
Response (200):
{
    "type": "post",
    "id": "https://app-chatbyte.herokuapp.com/author/7/posts/122ad56c-c153-4f60-9fa4-450c258df40e",
    "title": "test",
    "source": "https://app-chatbyte.herokuapp.com/author/7",
    "origin": "https://app-chatbyte.herokuapp.com/",
    "description": "test",
    "contentType": "text",
    "content": "test",
    "author": {
        "type": "author",
        "id": "https://app-chatbyte.herokuapp.com/author/7",
        "host": null,
        "displayName": "choo",
        "url": null,
        "github": null
    },
    "categories": [
        "text/plain"
    ],
    "count": 4,
    "size": 0,
    "comment_url": "",
    "comments": [
        "dc891869-8a7e-4496-8a0f-6443b83597d9"
    ],
    "published": "2021-04-01T09:37:19Z",
    "visibility": "public",
    "unlisted": "false"
}
```
#### `POST`
```
URL://service/author/{AUTHOR_ID}/posts/{POST_ID}
```
Response (200): updated post JSON object
```
{
    "type": "post",
    "id": "https://app-chatbyte.herokuapp.com/author/7/posts/122ad56c-c153-4f60-9fa4-450c258df40e",
    "title": "test",
    "source": "https://app-chatbyte.herokuapp.com/author/7",
    "origin": "https://app-chatbyte.herokuapp.com/",
    "description": "testtestpost",
    "contentType": "text",
    "content": "test",
    "author": {
        "type": "author",
        "id": "https://app-chatbyte.herokuapp.com/author/7",
        "host": null,
        "displayName": "choo",
        "url": null,
        "github": null
    },
    "categories": [
        "text/plain"
    ],
    "count": 4,
    "size": 0,
    "comment_url": "",
    "comments": [
        "dc891869-8a7e-4496-8a0f-6443b83597d9"
    ],
    "published": "2021-04-01T09:37:19Z",
    "visibility": "public",
    "unlisted": "false"
}
```
- Supports Pagination through **query parameters**
    - page -> Default value is set to 1 if not provided
    - size -> Default value is set to 5 if not provided

#### `GET`
<i>Get all posts from one author Using AuthorId</i>

```
URL https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts
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


#### `DELETE`
<i>Delete A Post By PostId</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts/{POST_ID}
```

#### `PUT`
<i>Create A Post By PostId</i>
<br>
<i>Side Effect: Sends To Friend Inbox, Erase Own Post With Same PostId</i>
Body of Request:
```
{
    "type": "post",
    "id": "https://app-chatbyte.herokuapp.com/author/7/posts/3aacce7e-407c-4605-8f80-7b1b0a8de08fabc",
    "title": "choo",
    "source": "https://app-chatbyte.herokuapp.com/author/7",
    "origin": "https://app-chatbyte.herokuapp.com/",
    "description": "choo",
    "contentType": "text",
    "content": "choo",
    "author": {
        "type": "author",
        "id": "https://app-chatbyte.herokuapp.com/author/7",
        "host": null,
        "displayName": "choo",
        "url": null,
        "github": null
    },
    "categories": [
        "text/plain"
    ],
    "count": 0,
    "size": 0,
    "comment_url": "",
    "comments": [],
    "published": "2021-04-01T09:37:43.806644Z",
    "visibility": "public",
    "unlisted": "false"
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)
Allowed visibility: (public, friend, private)


### **Follower API**
### `GET`
<i>get a list of authors who are their followers</i>
```
URL: https://app-chatbyte.herokuapp.com/api/author/{AUTHOR_ID}/followers
GET: Response (200)
```
Response:
```
{
    "type": "followers",
    "items": [
        {
            "type": "author",
            "id": "https://app-chatbyte.herokuapp.com/author/1",
            "host": "https://app-chatbyte.herokuapp.com/",
            "displayName": "test",
            "url": "https://app-chatbyte.herokuapp.com/author/1",
            "github": "https://app-chatbyte.herokuapp.com/author/1"
        },
        {
            "type": "author",
            "id": "https://app-chatbyte.herokuapp.com/author/6",
            "host": null,
            "displayName": "testuser",
            "url": null,
            "github": null
        }
    ]
}
```

### `GET`
<i>GET a specific follower</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
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

### `POST`
<i>Add a follower</i>
```
URL: https://app-chatbyte.herokuapp.com/api/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
Response:
```
Response (200):
{
    "detail": "true"
}
```

### `DELETE`
<i>remove a follower</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
Response:
```
Response (200):
{
    "status": "true"
}
```

### **Friend API**
### `GET`
<i>get all friends of author</i>
```
URL: "https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/friends/
```
Response:
```
Response (200):
{
    "type": "friends",
    "items": [
        {
            "type": "author",
            "id": "https://app-chatbyte.herokuapp.com/author/6",
            "host": null,
            "displayName": "testuser",
            "url": null,
            "github": null
        },
        {
            "type": "author",
            "id": "https://app-chatbyte.herokuapp.com/author/7",
            "host": null,
            "displayName": "choo",
            "url": null,
            "github": null
        }
    ]
}
```



    
### **Comments API**
### `GET` 
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts/{POST_ID}/comments

Response(200):
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "type": "comment",
            "id": "55e4258c-cbdc-49e6-a4ae-a84a024189b9",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "comment": "test comment",
            "contentType": "text",
            "published": "2021-04-01T18:45:56Z"
        }
    ]
}
```

- Supports Pagination through **query parameters**
    - page -> Default value is set to 1 if not provided
    - size -> Default value is set to 5 if not provided

#### `POST`
<i>Create Comment on a Post</i>
```
URL://service/author/{AUTHOR_ID}/posts/{POST_ID}/comments
```
For remote Body of Request:
```
{
    "Content":"Sick Olde English",
    "contentType":"text/markdown",
}
```
Allowed Content Types: (text/plain,text/markdown, application/base64,image/png;base64,image/jpeg;base64)

```
Response:
{
    "type": "comment",
    "id": "http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c",
    "comment": "Sick Olde English",
    "contentType": "text/markdown",
    "published": "2015-03-09T13:07:04Z"
}
```


### **Likes API **
#### `Like Object format`
```
{
     "@context": "https://www.w3.org/ns/activitystreams",
     "summary": "Lara Croft Likes your post",         
     "type": "Like",
     "author": {
         "type":"author",
          "id":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "host":"http://127.0.0.1:8000/",
         "displayName":"Lara Croft",
         "url":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
         "github":"http://github.com/laracroft"
     },
     "object":"http://127.0.0.1:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
}

```
#### `GET`
<i>Get Likes for a Post</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts/{POST_ID}/likes
```
```
Response (200):
 [
        {
            "type": "like",
            "id": "530c2845-8bfb-40d0-bf2f-932698ca19b9",
            "summary": "Like",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "object": "Like",
            "context": "Like"
        }
    ]

```
<i>Get Likes for a Comment</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
```
```
Response (200):
       [
        {
            "type": "like",
            "id": "530c2845-8bfb-40d0-bf2f-932698ca19b9",
            "summary": "Like",
            "author": {
                "type": "author",
                "id": "https://chatbyte.herokuapp.com/author/1",
                "host": null,
                "displayName": "test",
                "url": null,
                "github": null
            },
            "object": "Like",
            "context": "Like"
        },
        {
            "type": "like",
            "id": "f716dbb1-43bb-4bfe-9804-2a68c13cf32e",
            "summary": "Like",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "object": "Like",
            "context": "Like"
        }
    ]
```
#### `POST`
<i>Create a Like for either a Post or a Comment</i>
<br>
<i>Side Effect: Sends To Inbox</i>
```
URL: //service/author/{AUTHOR_ID}/likes
```
```
Request Body:
Comment Object || Post Object

Depending on which is sent, a corresponding like will be created.
```



### **Liked API **
#### `Liked Object format`
```
{
    "type": "liked",
    "items": [
        {
            "type": "like",
            "id": "f716dbb1-43bb-4bfe-9804-2a68c13cf32e",
            "summary": "Like",
            "author": {
                "type": "author",
                "id": "https://app-chatbyte.herokuapp.com/author/1",
                "host": "https://app-chatbyte.herokuapp.com/",
                "displayName": "test",
                "url": "https://app-chatbyte.herokuapp.com/author/1",
                "github": "https://app-chatbyte.herokuapp.com/author/1"
            },
            "object": "Like",
            "context": "Like"
        }
    ]
}
```
#### `GET`
<i>Get Liked for an author</i>
```
URL: https://app-chatbyte.herokuapp.com/author/{AUTHOR_ID}/liked
```

