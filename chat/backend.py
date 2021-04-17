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


"""
design for handling updateUser request in view , to update info 
"""
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


"""
design for handling addFriend request in view , to update info 
"""
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


"""
design for handling deleteFriend request in view , to update info 
"""
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


"""
design for handling getFollowing request in view , to update info 
"""
def getFollowing(usr_id, following_id):
    try:
        user = User.objects.get(id=usr_id)
        following = User.objects.get(id=following_id)
        if following.profile in user.profile.followings.all(): return following
        return None
    except BaseException as e:
        print(e)
        return None


"""
design for handling getFriend request in view , to update info 
"""
def getFriend(usr_id, friend_id):
    try:
        user = User.objects.get(id=usr_id)
        friend = User.objects.get(id=friend_id)
        if friend.profile in user.profile.friends.all(): return friend
        return None
    except BaseException as e:
        print(e)
        return None


"""
design for handling getFriends request in view , to update info 
"""
def getFriends(usr_id):
    try:
        user = User.objects.get(id=usr_id)
        return user.profile.friends.all()
    except BaseException as e:
        print(e)
        return None


"""
design for handling addFollow request in view , to update info 
"""
def addFollow(usr_id, follow_id):
    user = User.objects.get(id=usr_id)
    follow = User.objects.get(id=follow_id)
    print(follow)
    user.profile.followings.add(follow.profile)
    follow.profile.followers.add(user.profile)
    user.save()
    follow.save()
    return True


"""
design for handling createFriendRequest  in view , to update info 
"""
def createFriendRequest(usr_id, friend_id):
    object = User.objects.get(id=usr_id)
    author = User.objects.get(id=friend_id)
    friendRequestObj = FriendRequest.objects.create(summary=author.profile.displayName + 'wants to add ' + object.profile.displayName + ' as friend', author=author, object=object)
    return friendRequestObj


"""
design for handling addFriendRequest  in view , to update info 
"""
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


"""
design for handling deleteFriendRequestin view , to update info 
"""
def deleteFriendRequest(usr_id, friend_request_id):
    try:
        user = User.objects.get(id=usr_id)
        friend_request = user.profile.friend_requests.get(id=friend_request_id)
        user.profile.friend_requests.remove(friend_request)
        user.save()
        return True
    except BaseException as e:
        print(e)
        return False


"""
design for handling addFriendViaRequest in view , to update info 
"""
def addFriendViaRequest(usr_id, friend_request_id):
    try:
        user = User.objects.get(id=usr_id)
        friend_request = user.profile.friend_requests.get(id=friend_request_id)
        addFriend(friend_request.object.id, friend_request.actor.id)
        return True
    except BaseException as e:
        print(e)
        return False


"""
design for handling getALLFriendRequests  in view , to update info 
"""
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


"""
design for handling updateProfile request in view , to update info 
"""
def updateProfile(id, display_name, email, url, github):
    # Please authenticate before calling this method
    try:
        user = User.objects.get(pk=id)
        profile = user.profile

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

# the flag design for reshare, if it is reshare, i need post.origin to be passed, 
def createPost(title, source, origin, description, content_type, content, author, categories, visibility, unlisted, reshareID=None):
    # Please authenticate before calling this method
    # here cateories passed is string
    categories_array = []
    categories_array.append(categories)


    try:
        post = Post.objects.create(title=title, source=source, origin=origin, description=description, contentType=content_type, content=content \
            , categories=categories_array, count=0, size=0, comment_url="", visibility=visibility, author=author, unlisted=(unlisted.lower() in ['true', '1', 't', 'y',]))
        # print(post.author)

        post.comment_url = post.id + "/comments/"


        # if it is not, means not None, and it is the original posting
        if not reshareID:
            post.origin = post.id
            post.source = post.id
        else:
            post.categories = categories_array

            post.origin = origin
            post.source = reshareID
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

'''
Design for update post, which do not allowed change other attr
'''
def updatePost(id, title, description, content_type, content):
    # Please authenticate before calling this method
    try:
        post = Post.objects.get(id=id)
        post.title = title
        post.description = description
        post.contentType = content_type
        post.content = content

        post.save()
        return True
    except BaseException as e:
        print(e)
        return False


"""
design for handling editPostDescription request in view , to update info 
"""
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


"""
design for handling deletePost request in view , to update info 
"""
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
        return commentObj
    except BaseException as e:
        print(repr(e))
        traceback.print_exc()
        print(e)
        return False


"""
design for handling updateComment request in view , to update info 
"""
def updateComment(id):
    # Please authenticate before calling this method
    try:
        comment = Comment.objects.filter(id=id)[0]

        # update field here
        comment.save()
        return True
    except BaseException as e:
        print(e)
        return False

"""
design for handling deleteComment request in view , to update info 
"""
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


"""
design for handling getUser request in view , to update info 
"""
def getUser(usr_id):
    try:
        user = User.objects.get(id=usr_id)
        return user
    except BaseException as e:
        print(e)
        return None


"""
design for handling likePost request in view , to update info 
"""
def likePost(post_id, author_id):

    try:

        user_profile = Profile.objects.get(id=author_id)
        summary = user_profile.displayName +" Likes your post"
        new_like = Like.objects.create(author=user_profile, object=post_id, summary= summary)
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


"""
design for handling likeComment request in view , to update info 
"""
# TODO: check if remote, currently handling in fornt end
def likeComment(comment_id, author_id):


    try:
        user_profile = Profile.objects.get(id=author_id)
        summary = user_profile.displayName +" likes your comment"
        new_like = Like.objects.create(author=user_profile, object=comment_id, summary= summary)
        user_liked = user_profile.liked
        items_list = user_liked.items
        items_list.add(new_like)
        comment = Comment.objects.get(id=comment_id)
        comment.likes.add(new_like)
        comment.save()
        user_profile.liked.save()

    except BaseException as e:
        print(e)
        return None
