
from .models import Post, Comment, Profile
import datetime
from django.conf import settings
from django.contrib.auth.models import User

# def setCookie(response, key, value, days_expire=1):
#     # https://stackoverflow.com/questions/1622793/django-cookies-how-can-i-set-them
#     if days_expire is None:
#         max_age = 365 * 24 * 60 * 60  # one year
#     else:
#         max_age = days_expire * 24 * 60 * 60
#     expires = datetime.datetime.strftime(
#         datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
#         "%a, %d-%b-%Y %H:%M:%S GMT",
#     )
#     response.set_cookie(
#         key,
#         value,
#         max_age=max_age,
#         expires=expires,
#         domain=settings.SESSION_COOKIE_DOMAIN,
#         secure=settings.SESSION_COOKIE_SECURE or None,
#     )


def updateUser(username, password):
    # Please authenticate before calling this method
    try:
        actor = User.objects.filter(USERNAME=username)[0]
        actor.username = username
        actor.password = password
        actor.save()
        return True
    except BaseException as e:
        print(e)
        return False


# add friend
# def addFriend(name, friend_name):
#     try:
#         author = Author.objects.filter(DISPLAY_NAME=name)[0]
#         friend = Author.objects.filter(DISPLAY_NAME=friend_name)[0]
#         author.FRIENDS.add(friend)
#         return True
#     except BaseException as e:
#         print(e)
#         return False

def updateProfile(id, first_name, last_name, email, url, github):
    # Please authenticate before calling this method
    try:
        user = User.objects.get(pk=id)
        profile = Profile.objects.get(pk=id)
        # update element here
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.URL = url
        profile.GITHUB = github

        user.save()
        profile.save()
        return True
    except BaseException as e:
        print(e)
        return False

def createPost(title, source, origin, description, content_type, content, author, categories, visibility):
    # Please authenticate before calling this method
    try:
        post = Post.objects.create(TITLE=title, SOURCE=source, ORIGIN=origin, DESCRIPTION=description, CONTENT_TYPE=content_type, CONTENT=content \
            , AUTHOR=author, CATEGORIES=categories, COUNT=0, SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY=visibility)
        author.profile.TIMELINE.add(post)
        author.save()
        return True
    except BaseException as e:
        print(e)
        return False

def updatePost(id, title, source, origin, description, content_type, content, categories, visibility):
    # Please authenticate before calling this method
    try:
        post = Post.objects.get(ID=id)
        print("old title:", post.TITLE)
        post.TITLE = title
        
        post.SOURCE = source
        post.ORIGIN = origin
        post.DESCIPTION = description
        post.CONTENT_TYPE = content_type
        post.CONTENT = content
        # post.author = author
        post.CATEGORIES = categories
        post.VISIBILITY = visibility

        post.save()
        return True
    except BaseException as e:
        print(e)
        return False

def editPostDescription(id, description):
    # Please authenticate before calling this method
    try:
        post = Post.objects.get(ID=id)
        post.DESCRIPTION = description
        if 'text/' in post.CATEGORIES:
            post.CONTENT = description
        post.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deletePost(id):
    # Please authenticate before calling this method
    try:
        Post.objects.get(ID=id).delete()
        return True
    except BaseException as e:
        print(e)
        return False


def createComment(author, post_id, comment, content_type):
    try:
        post = Post.objects.get(ID=post_id)
        commentObj = Comment.objects.create(AUTHOR=author, COMMENT=comment, CONTENT_TYPE=content_type)
        post.COMMENTS.add(commentObj)
        print('comment:',commentObj)
        post.save()
        return True
    except BaseException as e:
        print(e)
        return False

def updateComment(id):
    # Please authenticate before calling this method
    try:
        comment = Comment.objects.filter(ID=id)[0]
        # print('====comment====', comment)
        # update field here
        comment.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deleteComment(id):
    # Please authenticate before calling this method
    try:
        Comment.objects.filter(ID=id).delete()
        return True
    except BaseException as e:
        print(e)
        return False

# get post funcountion
def getPost(post_id):
    try:
        post = Post.objects.get(pk=post_id)
        return post
    except BaseException as e:
        print(e)
        return None
# get post comment
def getComments(post_id):
    try:
        post = getPost(post_id)
        comments = post.COMMENTS.all()
        return comments
    except BaseException as e:
        print(e)
        return None