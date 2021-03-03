from .models import Author, Post, Comment, User


# connec to db , validate user
def createUser(username, password, host, url, github):
    try:
        User.objects.create(USERNAME=username, PASSWORD=password)
        createAuthor(host, username, url, github)
        return True
    except:
        return False

def validUser(username, password):
    try:
        user = User.objects.filter(USERNAME=username)
        if password == user.PASSWORD:
            return True
        else:
            return False
    except:
        return False

def addToFriendRequest(name, friend_name):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        friend = Author.objects.filter(DISPLAY_NAME=friend_name)
        author.FRIEND_REQUESTS.add(friend)
        return True
    except:
        return False

def addToFollowers(name, friend_name):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        friend = Author.objects.filter(DISPLAY_NAME=friend_name)
        author.FOLLOWERS.add(friend)
        return True
    except:
        return False

def addToTimeline(name, post):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        author.TIMELINE.add(post)
        return True
    except:
        return False

# add as friend 
def addToFriends(name, friend_name):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        friend = Author.objects.filter(DISPLAY_NAME=friend_name)
        author.FRIENDS.add(friend)
        return True
    except:
        return False

def getTimeline(name):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        return author.TIMELINE
    except:
        return None

def getAuthor(name):
    try:
        return Author.objects.filter(DISPLAY_NAME=name)
    except:
        return None

def createAuthor(host, display_name, url, github):
    try:
        Author.objects.create(HOST=host, DISPLAY_NAME=display_name, URL=url, GITHUB=github)
        return True
    except:
        return False

def updateAuthor(name):
    #TODO
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)
        # update element here
        author.save()
        return True
    except:
        return False

def deleteAuthor(name):
    try:
        Author.objects.filter(DISPLAY_NAME=name).delete()
        return True
    except:
        return False

def createPost(title, source, origin, description, content_type, content, author, categories, visibility):
    #TODO keep track of COMMENTS_NO and PAGE_SIZE, COMMENTS_FIRST_PAGE
    try:
        Post.objects.create(TITLE=title, SOURCE=source, ORIGIN=origin, DESCIPTION=description, CONTENT_TYPE=content_type, CONTENT=content \
            , AUTHOR=author, CATEGORIES=categories, COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY=visibility)
        return True
    except:
        return False

def updatePost(id):
    #TODO
    try:
        post = Post.objects.filter(ID=id)
        # update field here
        post.save()
        return True
    except:
        return False

def deletePost(id):
    try:
        Post.objects.filter(ID=id).delete()
        return True
    except:
        return False

def createComment(author, comment, comment_type):
    try:
        Comment.objects.create(AUTHOR=author, COMMENT=comment, COMMENT_TYPE=comment_type)
        return True
    except:
        return False

def updateComment(id):
    #TODO
    try:
        comment = Comment.objects.filter(ID=id)
        # update field here
        comment.save()
        return True
    except:
        return False

def deleteComment(id):
    try:
        Comment.objects.filter(ID=id).delete()
        return True
    except:
        return False