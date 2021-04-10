from rest_framework.serializers import Serializer
from .models import Post, Comment, Profile, Follower, FriendRequest, Like, Liked
import datetime
from django.conf import settings
import django
from django.contrib.auth.models import User
import traceback
from .signals import host
from .serializers import PostSerializer, ProfileSerializer
from requests.auth import HTTPBasicAuth
from .remoteProxy import inboxRequest

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
# def getUser(usr_id):
#     return User.objects.get(id=usr_id)

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
        user.profile.friends.add(friend.profile)
        friend.profile.friends.add(user.profile)

        user.save()
        friend.save()
        return True
    except BaseException as e:
        print(e)
        return False

def deleteFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        user.profile.friends.remove(friend.profile)
        user.save()
        return True
    except BaseException as e:
        print(e)
        return False

def getFollowing(usr_id, following_id):
    try:
        user = User.objects.get(id=usr_id)
        following = User.objects.get(id=following_id)
        if following.profile in user.profile.followings.all(): return following
        return None
    except BaseException as e:
        print(e)
        return None

def getFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        if friend.profile in user.profile.friends.all(): return friend
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

def addFollow(usr_id, follow_id):
    user = User.objects.get(id=usr_id)
    follow = User.objects.get(id=follow_id)
    print(follow)
    user.profile.followings.add(follow.profile)
    follow.profile.followers.add(user.profile)
    user.save()
    follow.save()
    return True


def createFriendRequest(usr_id, friend_id):
    object = User.objects.get(id=usr_id)
    author = User.objects.get(id=friend_id)
    friendRequestObj = FriendRequest.objects.create(summary=author.profile.displayName + 'wants to add ' + object.profile.displayName + ' as friend', author=author, object=object)
    return friendRequestObj

def addFriendRequest(usr_id, friend_id):
    try:
        object = User.objects.get(id=usr_id)
        author = User.objects.get(id=friend_id)
        friendRequestObj = FriendRequest.objects.create(summary="", actor=author.profile, object=object.profile)
        object.profile.friend_requests.add(friendRequestObj)
        author.profile.friend_requests_sent.add(friendRequestObj)
        object.save()
        author.save()
        return True
    except BaseException as e:
        print(e)
        return False


def deleteFriendRequest(usr_id, friend_request_id):
    try:
        user = User.objects.get(id=usr_id)
        # friend = User.objects.get(id=friend_id)
        friend_request = user.profile.friend_requests.get(id=friend_request_id)
        user.profile.friend_requests.remove(friend_request)
        user.save()
        return True
    except BaseException as e:
        print(e)
        return False

def addFriendViaRequest(usr_id, friend_request_id):
    try:
        user = User.objects.get(id=usr_id)
        friend_request = user.profile.friend_requests.get(id=friend_request_id)
        # print(friend_request)
        # friend_profile = friend_request.actor
        # user_profile = friend_request.object
        addFriend(friend_request.object.id, friend_request.actor.id)
        return True
    except BaseException as e:
        print(e)
        return False

def getALLFriendRequests(usr_id):

    print("getALLFriendRequests")

    try:
        user = User.objects.get(id=usr_id)
        # print(user.profile.friend_requests.all())
        print("try")
        print(user.inbox.friend_requests)
        return user.inbox.friend_requests.all()
    except BaseException as e:
        print(e)
        return None


def updateProfile(id, display_name, email, url, github):
    # Please authenticate before calling this method
    try:
        user = User.objects.get(pk=id)
        profile = user.profile
        # profile = Profile.objects.get(pk=id)
        # update element here
        # user.first_name = first_name
        # user.last_name = last_name
        user.email = email
        profile.url = url
        profile.github = github
        profile.displayName = display_name
        user.save()
        profile.save()
        return True
    except BaseException as e:
        print(e)
        return False

def createPost(title, source, origin, description, content_type, content, author, categories, visibility, unlisted):
    # Please authenticate before calling this method
    try:
        post = Post.objects.create(title=title, source=source, origin=origin, description=description, contentType=content_type, content=content \
            , categories=categories, count=0, size=0, comment_url="", visibility=visibility, author=author, unlisted=(unlisted.lower() in ['true', '1', 't', 'y',]))
        # print(post.author)

        post.comment_url = post.id + "/comments/"
        post.source = post.id
        post.save()
        author.timeline.add(post)
        author.save()

        
        # Broadcast to friends
        if (visibility == 'friend'):
            print("Broadcasting post to friends...")
            for friend_profile in author.friends.all():
                print(friend_profile.id)
                author_id = friend_profile.id.split('author/')[1]
                
                server_origin = friend_profile.id.split("author/")[0]
                if server_origin == host:
                    print("doing locally")
                    # send post to inbox
                    friend_profile.user.inbox.post_inbox.items.add(post)
                    # add post into timeline
                    friend_profile.timeline.add(post)
                else:
                    serializer = PostSerializer(post)
                    post_serialize = serializer.data
                    author_serialize = ProfileSerializer(post.author)
                    post_serialize['author'] = author_serialize.data
                    print(post_serialize)
                    # send post to remote inbox
                    inboxRequest("POST", server_origin, author_id, post_serialize)
            print("done")
        return True
    except BaseException as e:
        print(repr(e))
        traceback.print_exc()
        print(e)
        return False

def updatePost(id, title, source, origin, description, content_type, content, categories, visibility):
    # Please authenticate before calling this method
    try:
        print("here")
        post = Post.objects.get(id=id)
        print("old id:", id)
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

'''
Design for create comment, here author is a profile
'''
def createComment(author, post_id, comment, content_type, published=django.utils.timezone.now()):
    try:
        post = Post.objects.get(id=post_id)
        commentObj = Comment.objects.create(author=author, comment=comment, contentType=content_type, published=published, parent_post=post)
        post.comments.add(commentObj)
        print("post_count:", post.count)
        post.count += 1
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

def getUser(usr_id):
    try:
        user = User.objects.get(id=usr_id)
        return user
    except BaseException as e:
        print(e)
        return None

def likePost(post_id, author_id):

    print("________post_id__", post_id)
    print("author_id  ", author_id)
    try:
        user_profile = Profile.objects.get(id=author_id)
        new_like = Like.objects.create(author=user_profile, object=post_id)
        user_liked = user_profile.liked
        items_list = user_liked.items
        items_list.add(new_like)
        post = Post.objects.get(id=post_id)
        post.likes.add(new_like)
        post.save()
        user_profile.liked.save()

    except BaseException as e:
        print(e)
        return None 
        
    # TODO: check if remote
def likeComment(comment_id, author_id):
    # TODO
    pass