### **Author Profile API**
```
URL: ://service/author/{AUTHOR_ID}/
GET: retrieve their profile
POST: update profile
```

### **Stream API**
### `GET`
<i>GET USER Stream with Pagination</i>
```
URL: ://service/author/{AUTHOR_ID}/followers
```

### **Inbox API**
<i>GET USER notifications</i>
```
URL: ://service/author/<str:AUTHOR_ID>/inbox/
```
### **Follower API**
### `GET`
<i>get a list of authors who are their followers</i>
```
URL: ://service/author/{AUTHOR_ID}/followers
GET:
POST:
DELETE:
```

### `GET`
<i>check if follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
### `PUT`
<i>Add a follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```
### `DELETE`
<i>remove a follower</i>
```
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
```

### **Friend API**
### `GET`
<i>get all friends of author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```

### `POST`
<i>add a friend to author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```

### `DELETE`
<i>delete a friend from author</i>
```
URL: ://service/author/{AUTHOR_ID}/friends/
```

### `GET`
<i>get all authors has the author as friend</i>
```
URL: ://service/author/asFriend/<query: url=<url of the author>>
```

#### `GET`
<i>Get comments for a Post</i>
```
URL: //service/author/{AUTHOR_ID}/posts/{POST_ID}/comments
```

#### `POST`
<i>Create Comment on a Post</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/comments
```

#### `GET`
<i>Get Likes for a Post</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}/likes
```
#### `POST`
<i>Create a Like for either a Post or a Comment</i>
<br>
<i>Side Effect: Sends To Inbox</i>
```
://service/author/{AUTHOR_ID}/likes
```
#### `GET`
<i>Get Liked for an author</i>
```
://service/author/{AUTHOR_ID}/liked
```
#### `GET`

<i>Get Post Using PostId</i>

```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
```

<i>Get Post Using AuthorId</i>

```
://service/author/{AUTHOR_ID}/posts/
```

<i>Get Stream Using AuthorId</i>

```
://service/author/{AUTHOR_ID}/stream
```

#### `POST`
<i>Create A Post By AuthorId</i>
<br>
<i>Side Effect: Sends To Friend Inbox</i>

```
://service/author/{AUTHOR_ID}/posts/
```

<i>Edit A Post By AuthorId</i>

```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
```

#### `DELETE`
<i>Delete A Post By PostId</i>
```
://service/author/{AUTHOR_ID}/posts/{POST_ID}
``
