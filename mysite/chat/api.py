from .models import Author, Post, Comment, Actor


# connec to db , validate user
def createActor(username, password):
    try:
        Actor.objects.create(USERNAME=username, PASSWORD=password)
        return True
    except:
        return False

def validActor(username, password):
    try:
        actor = Actor.objects.filter(USERNAME=username)[0]
        if password == actor.PASSWORD:
            return True
        else:
            return False
    except:
        return False

# add friend 
def addFriend(name, friend_name):
    try:
        author = Author.objects.filter(DISPLAY_NAME=name)[0]
        friend = Author.objects.filter(DISPLAY_NAME=friend_name)[0]
        author.FRIENDS.add(friend)
        return True
    except:
        return False

def getTimeline(id):
    # need to change to user name
    try:
        author = Author.objects.filter(ID=id)
        return author.TIMELINE
    except:
        return None

def getAuthor(name):
    try:
        return Author.objects.filter(DISPLAY_NAME=name)[0]
    except:
        return None

def createAuthor(host, display_name, url, github):
    try:
        Author.objects.create(HOST=host, DISPLAY_NAME=display_name, URL=url, GITHUB=github)
        return True
    except:
        return False

def updateAuthor(id):
    #TODO
    try:
        author = Author.objects.filter(ID=id)
        # update element here
        author.save()
        return True
    except:
        return False

def deleteAuthor(id):
    try:
        Author.objects.filter(ID=id).delete()
        return True
    except:
        return False

def createPost(title, source, origin, description, content_type, content, author, categories, visibility):
    #TODO keep track of COMMENTS_NO and PAGE_SIZE, COMMENTS_FIRST_PAGE
    try:
        post = Post.objects.create(TITLE=title, SOURCE=source, ORIGIN=origin, DESCIPTION=description, CONTENT_TYPE=content_type, CONTENT=content \
            , AUTHOR=author, CATEGORIES=categories, COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY=visibility)
        author.TIMELINE.add(post)
        author.save()
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