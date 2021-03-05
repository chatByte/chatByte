from .models import Author, Post, Comment, Actor
import datetime
from django.conf import settings

def setCookie(response, key, value, days_expire=1):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )

# connec to db , validate user
def createActor(username, password):
    try:
        Actor.objects.create(USERNAME=username, PASSWORD=password)
        return True
    except:
        return False

def updateActor(username, password):
    try:
        actor = Actor.objects.filter(USERNAME=username)[0]
        actor.USERNAME = username
        actor.PASSWORD = password
        actor.save()
        return True
    except:
        return False

def getActor(username):
    try:
        actor = Actor.objects.filter(USERNAME=username)[0]
        return actor
    except:
        return None

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
    except BaseException as e:
        print(e)
        return False

def getTimeline(username):
    # need to change to usp zer name
    try:
        author = Author.objects.filter(DISPLAY_NAME=username)[0]
        return author.TIMELINE.all()
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

def updateAuthor(username, host, url, github):
    #TODO
    try:
        author = Author.objects.filter(DISPLAY_NAME=username)[0]
        # update element here
        author.DISPLAY_NAME = username
        author.HOST = host
        author.URL = url
        author.GITHUB = github

        # author.PASSWORD = password

        author.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deleteAuthor(username):
    try:
        Author.objects.filter(DISPLAY_NAME=username).delete()
        return True
    except Exception as e:
        # print(e, '-----------')
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

def updatePost(id, title, source, origin, description, content_type, content, categories, visibility):
    # title, source, origin, description, content_type, content, author, categories, visibility
    try:
        post = Post.objects.filter(ID=id)[0]
        post.title = title
        post.source = source
        post.origin = origin
        post.description = description
        post.content_type = content_type
        post.contetn = content
        # post.author = author
        post.categories = categories
        post.visibility = visibility
        
        post.save()
        return True
    except Exception as e:
        print(e, '*********************')
        return False

def deletePost(id):
    try:
        Post.objects.filter(ID=id).delete()
        return True
    except:
        return False

def createComment(author, comment, content_type):
    try:
        commentObj = Comment.objects.create(AUTHOR=author, COMMENT=comment, CONTENT_TYPE=content_type)
        # print('comment:',commentObj)
        return True
    except Exception as e:
        # print(e, '*******')
        return False

def updateComment(id):
    #TODO
    try:
        comment = Comment.objects.filter(ID=id)[0]
        # print('====comment====', comment)
        # update field here
        comment.save()
        return True
    except Exception as e:
        # print(e, '*********************')
        return False

def deleteComment(id):
    try:
        Comment.objects.filter(ID=id).delete()
        return True
    except Exception as e:
        # print(e, '*********************')
        return False