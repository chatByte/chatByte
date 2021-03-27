
from .models import Post, Comment, Profile, Followers, FriendRequest, Like, Liked
import datetime
from django.conf import settings
import django
from django.contrib.auth.models import User
import traceback

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
def getUser(usr_id):
    return User.objects.get(id=usr_id)

def updateUser(username, password):
    # Please authenticate before calling this method
    try:
        actor = User.objects.filter(username=username)[0]
        actor.username = username
        actor.password = password
        actor.save()
        return True
    except BaseException as e:
        print(e)
        return False


def addFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        # mutual friend
        user.profile.friends.add(friend)
        friend.profile.friends.add(user)
        # mutual followers
        user.profile.followers.add(friend)
        friend.profile.followers.add(user)

        user.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deleteFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        user.profile.friends.remove(friend)
        user.save()
        return True
    except BaseException as e:
        print(e)
        return False

def getFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        if friend in user.profile.friends.all(): return friend
        return None
    except BaseException as e:
        print(e)
        return None

def getFriends(usr_id):
    try:
        user = User.objects.get(id=usr_id)
        return user.profile.friends.all()
    except BaseException as e:
        print(e)
        return None

def createFriendRequest(usr_id, friend_id):
    object = User.objects.get(id=usr_id)
    author = User.objects.get(id=friend_id)
    friendRequestObj = FriendRequest.objects.create(summary=author.profile.displayName + 'wants to add ' + object.profile.displayName + ' as friend', author=author, object=object)
    return friendRequestObj

def addFriendRequest(usr_id, friend_id):
    try:
        object = User.objects.get(id=usr_id)
        author = User.objects.get(id=friend_id)
        friendRequestObj = FriendRequest.objects.create(summary="", author=author, object=object)
        object.profile.friend_requests.add(friendRequestObj)
        author.profile.friend_requests_sent.add(friendRequestObj)
        object.save()
        return True
    except BaseException as e:
        print(e)
        return False


def deleteFriendRequest(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        user.profile.friend_requests.remove(friend)
        user.save()
        return True
    except BaseException as e:
        print(e)
        return False

def getALLFriendRequests(usr_id):
    try:
        user = User.objects.get(id=usr_id)
        print(user.profile.friend_requests.all())
        return user.profile.friend_requests.all()
    except BaseException as e:
        print(e)
        return None


def updateProfile(id, first_name, last_name, email, url, github):
    # Please authenticate before calling this method
    try:
        user = User.objects.get(pk=id)
        profile = Profile.objects.get(pk=id)
        # update element here
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        profile.url = url
        profile.github = github

        user.save()
        profile.save()
        return True
    except BaseException as e:
        print(e)
        return False

def createPost(title, source, origin, description, content_type, content, author, categories, visibility):
    # Please authenticate before calling this method
    try:
        post = Post.objects.create(title=title, source=source, origin=origin, description=description, contentType=content_type, content=content \
            , categories=categories, count=0, size=0, commentsPage='0', visibility=visibility, author=author)
        print(post.author)
        author.timeline.add(post)
        author.save()
        return True
    except BaseException as e:
        print(repr(e))
        traceback.print_exc()
        print(e)
        return False

def updatePost(id, title, source, origin, description, content_type, content, categories, visibility):
    # Please authenticate before calling this method
    try:
        post = Post.objects.get(id=id)
        print("old title:", post.title)
        post.title = title

        post.source = source
        post.origin = origin
        post.description = description
        post.contentType = content_type
        post.content = content
        # post.author = author
        post.categories = categories
        post.visibility = visibility
        post.save()
        return True
    except BaseException as e:
        print(e)
        return False

def editPostDescription(id, description):
    # Please authenticate before calling this method
    try:
        post = Post.objects.get(id=id)
        post.description = description
        if 'text/' in post.categories:
            post.content = description
        post.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deletePost(id):
    # Please authenticate before calling this method
    try:
        Post.objects.get(id=id).delete()
        return True
    except BaseException as e:
        print(e)
        return False


def createComment(author, post_id, comment, content_type, published=django.utils.timezone.now()):
    try:
        post = Post.objects.get(id=post_id)
        print(post)
        commentObj = Comment.objects.create(author=author, comment=comment, contentType=content_type, published=published)
        post.comments.add(commentObj)
        print('comment:',commentObj)
        post.save()
        return True
    except BaseException as e:
        print(repr(e))
        traceback.print_exc()
        print(e)
        return False


# # designed for api.py send json obj
# def createComment_obj(author, post_id, comment, content_type, published):
#     try:
#         post = Post.objects.get(id=post_id)
#         commentObj = Comment.objects.create(author=author, comment=comment, contentType=content_type)
#         post.comments.add(commentObj)
#         print('comment:',commentObj)
#         post.save()
#         return True
#     except BaseException as e:
#         print(repr(e))
#         traceback.print_exc()
#         print(e)
#         return False



def updateComment(id):
    # Please authenticate before calling this method
    try:
        comment = Comment.objects.filter(id=id)[0]
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
        Comment.objects.filter(id=id).delete()
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
        comments = post.comments.all()
        return comments
    except BaseException as e:
        print(e)
        return None
