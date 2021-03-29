from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import *
from .serializers import *
from .backend import *
import os
from .remoteProxy import *
from .signals import host as host_server

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# queryset = Post.objects.all()
# serializer_class = PostSerializer


# @login_required
# @require_http_methods(["GET", "POST", "PUT", "DELETE"])
# def post_obj(request, AUTHOR_ID, POST_ID):
#     cur_user_name = None
#     if request.user.is_authenticated:
#         cur_user_name = request.user.username
#     # post_id = request.build_absolute_uri().split("/")[-2][6:]

#     if request.method == "DELETE":
#         deletePost(POST_ID)
#         response = redirect("../posts/")
#         return response
#     elif request.method == "GET":
#         post = getPost(POST_ID)
#         # TODO return an object or html?
#         return post
#     elif request.method == "POST":
#         # updatePost()
#         pass





'''
Testing method

{
    "type": "post",
    "id": "3",
    "title": "fffffffffff",
    "source": "https://chatbyte.herokuapp.com/",
    "origin": "https://chatbyte.herokuapp.com/",
    "description": "asdf",
    "contentType": "text",
    "content": "asdf",
    "author": {
        "type": "author",
        "id": "2",
        "host": null,
        "displayName": "test",
        "url": "https://chatbyte.herokuapp.com/chat/author/2/profile/",
        "github": "https://github.com/Jeremy0818"
    },
    "categories": "text/plain",
    "count": 1,
    "size": 1,
    "commentsPage": "1",
    "comments": [],
    "published": "2021-03-26T19:04:53Z",
    "visibility": "public",
    "unlisted": "false"
}

'''


# No CSRF token
@csrf_exempt
# methdo
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# which AUTH using right now
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
# permission, -> auth
@permission_classes([IsAuthenticated])
def post_obj(request, AUTHOR_ID, POST_ID):


    # ex. equest.META[Origin] == ("https:\\chatbyte"):
    # req_origin = request.META["Origin"] 
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)
    user_origin = request.META["X-request-User"]

    if user_origin != host_server :
        return postRequest(request.method,user_origin, AUTHOR_ID, POST_ID)
    else:
        if request.method == "DELETE":
            # remove the post
            try:
                Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            deletePost(POST_ID)
            return JsonResponse({'status':'true','message':'successful'}, status=204)
        elif request.method == "GET":
            # get the public post
            try:
                post = Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data)
        elif request.method == 'POST':
            # update the post
            try:
                post = Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            data = JSONParser().parse(request)
            serializer = PostSerializer(post, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        elif request.method == 'PUT':
            # create a post with that post_id
            try:
                post = Post.objects.get(id=POST_ID)
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' already exists'}, status=409)
            except Post.DoesNotExist:
                pass
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializers.id = POST_ID
                profile = Profile.objects.get(pk=AUTHOR_ID)
                serializer.save(author=profile)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)




#author/<str:AUTHOR_ID>/posts/'
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def posts_obj(request, AUTHOR_ID):
    # ex. equest.META[origin] == ("https:\\chatbyte"):
    req_origin = request.META["Origin"] 
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if req_origin != host_server :
        return postsRequest(request.method,req_origin, AUTHOR_ID)
    else:
        if request.method == 'GET':
            profile = Profile.objects.get(id=AUTHOR_ID)
            posts = profile.timeline
            serializer = PostSerializer(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                profile = Profile.objects.get(id=AUTHOR_ID)
                serializer.save(author=profile)
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)




'''
Tetsing format: 
http://127.0.0.1:8000/chat/author/1/posts/3d93a8ea-3175-4e75-b1ae-03655c663b75/comments/

{
    "type":"comment",
      "author":{
        "type":"author",
        "id":1,
        "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
          "host":"http://127.0.0.1:5454/",
          "displayName":"Greg Johnson",
          "github": "http://github.com/gjohnson"
    },
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    "published":"2015-03-09T13:07:04+00:00",
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
}
     
'''

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_obj(request, AUTHOR_ID, POST_ID):
    '''
    Get conmments  for a Post
    Response Object Structure: [list of Like objects] using json
    '''


    # ex. equest.META[origin] == ("https:\\chatbyte"):
    req_origin = request.META["Origin"] 
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)

    if req_origin != host_server :
        return commentRequest(request.method,req_origin, AUTHOR_ID, POST_ID)
    else:
        # checking, comments' father exist or not
        try:
            post = Post.objects.get(id=POST_ID)
        except Post.DoesNotExist:
            return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
        if request.method == 'GET':
            # list obj contain a list of comment    
            comments = post.comments
            serializer = CommentSerializer(comments, many=True)
            return JsonResponse(serializer.data, safe=False)

        elif request.method == 'POST':
            # cretate comment
            data = JSONParser().parse(request)

            serializer = CommentSerializer(data=data)
            if serializer.is_valid():

                # save comments to post obj, update
                # post.comments.add
                # post_serializer = PostSerializer(post, data=data)
                # if post_serializer.is_valid(raise_exception=True):
                #     post_serializer.save()
                # may be we should user seralzier to test profile obj, and post obj
                # ex: post_serializer.errors?
                profile_obj = Profile.objects.get(id=AUTHOR_ID)

                if (createComment(profile_obj, POST_ID, data["comment"], data["contentType"], data["published"])):

                    return JsonResponse(serializer.data, status=201)
                else:
                    return JsonResponse(serializer.data, status=403)

        # elif request.method == "DELETE":
        #     # TODO
        #     pass
            
        return JsonResponse(serializer.errors, status=400)

'''
Tetsing format: 
  "author":{
    "type":"author",
    "id":1,
    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
    "host":"http://127.0.0.1:5454/",
    "displayName":"Greg Johnson",
    "github": "http://github.com/gjohnson"
}
'''
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile_obj(request, AUTHOR_ID):
    """
    REST Author, Generate response at my profile page ,
    """

    # ex. equest.META[origin] == ("https:\\chatbyte"):
    req_origin = request.META["Origin"] 
    print("Origin: ", host_server)
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if req_origin != host_server :
        print("origin is different, going to remote...")
        return profileRequest(request.method,req_origin, AUTHOR_ID)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        # query to database
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return JsonResponse(serializer.data)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            serializer = ProfileSerializer(profile, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            return JsonResponse(serializer.errors, status=400)
            # post_obj = json.loads(request.body)
            # url = post_obj["url"]
            # displayName = post_obj["displayName"]
            # github = post_obj["github"]
            # # we do not allowed leave our server
            # # host = post_obj["host"]
            # updateProfile(displayName, url, github)
            # return post_obj





'''

URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'GET', 'DELETE'])
def follower_obj(request, AUTHOR_ID, FOREIGN_AUTHOR_ID):
    # ex. request.META[origin] == ("https:\\chatbyte"):
    req_origin = request.META["Origin"] 
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    FOREIGN_AUTHOR_ID = host_server + "/posts/" + FOREIGN_AUTHOR_ID
    print("post id: ", FOREIGN_AUTHOR_ID)

    if req_origin != host_server :
        return followerRequest(request.method,req_origin, AUTHOR_ID, FOREIGN_AUTHOR_ID)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=AUTHOR_ID)
        except profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)


        if (request.method == "GET"):
            #reponse a follower
            try:
                follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)                
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'FOREIGN_AUTHOR_ID: ' + FOREIGN_AUTHOR_ID + ' does not exists'}, status=404)

            serializer = ProfileSerializer(follower)

            if serializer.is_valid(raise_exception=True):
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)


        elif (request.method == "PUT"):
            #add a follower , with FOREIGN_AUTHOR_ID
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=200)

            try:
                follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)  
                return JsonResponse({'detail': 'true'}, status=409)


            except Profile.DoesNotExist:
               profile.followers.add(follower)

               profile.save()

               return JsonResponse({}, status=201)


        elif request.method == "DELETE":
            profile.followers.remove(follower)
            return JsonResponse({}, status=200)

        return JsonResponse(serializer.errors, status=400)



'''
# URL: ://service/author/{AUTHOR_ID}/followers/
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def followers_obj(request, AUTHOR_ID):
    # ex. equest.META[origin] == ("https:\\chatbyte"):
    req_origin = request.META["Origin"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if req_origin != host_server :
        return followersRequest(request.method,req_origin, AUTHOR_ID)
    else:
        try:
            profile = Profile.objects.get(user_id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        followers = profile.followers
        serializer = FollowerSerializer(followers, many=True)
        if request.method == "GET":
            if serializer.is_valid(raise_exception=True):
                return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)




# @csrf_exempt
# @authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# @api_view(['POST'])
# def add_friend_obj(request, AUTHOR_ID, FRIEND_ID):
#     return None




@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_friends_obj(request, AUTHOR_ID):
    req_origin = request.META["Origin"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if req_origin != host_server :
        return friendsRequest(request.method,req_origin, AUTHOR_ID)
    else:
        try:
            profile = Profile.objects.get(user_id=AUTHOR_ID)
        except profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        friends = profile.friends
        serializer = ProfileSerializer(friends, many=True)
        if request.method == "GET":
            if serializer.is_valid(raise_exception=True):
                return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
# out box friend request, ie. accept a friend requst for box
def befriend(request, AUTHOR_ID):
    data = JSONParser().parse(request)

    serializer = ProfileSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        friend_id = data['id']
        try:
            friend = Profile.objects.get(id=friend_id)
        except:
            serializer.save()
            friend = Profile.objects.get(id=friend_id)
        profile = Profile.objects.get(pk=AUTHOR_ID)
        profile.friends.add(friend)
        profile.friends.save()
        return JsonResponse(data, status=200)
    return JsonResponse(serializer.errors, status=400) 





'''
Get likes for a Post
Response Object Structure: [list of Like objects]
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def likes_post_obj(request, AUTHOR_ID, POST_ID):
    req_origin = request.META["Origin"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)

    if req_origin != host_server :
        return likesRequest(request.method, req_origin, AUTHOR_ID, POST_ID)
    else:
        try:
            post = Post.objects.get(pk=POST_ID)
        except Post.DoesNotExist:
            return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
        likes = post.likes
        serializer = LikeSerializer(likes, many=True)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def likes_comment_obj(request, AUTHOR_ID, POST_ID, COMMENT_ID):
    req_origin = request.META["Origin"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)
    COMMENT_ID = AUTHOR_ID + "/posts/" + POST_ID + "/comments/" + COMMENT_ID
    print("post id: ", COMMENT_ID)

    if req_origin != host_server :
        return likesRequest(request.method, req_origin, AUTHOR_ID, POST_ID, COMMENT_ID)
    else:
        try:
            comment = Comment.objects.get(pk=COMMENT_ID)
        except Comment.DoesNotExist:
            return JsonResponse({'status':'false','message':'comment id: ' + COMMENT_ID + ' does not exists'}, status=404)
        likes = comment.likes
        serializer = LikeSerializer(likes, many=True)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)



@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_post_obj(request, AUTHOR_ID):
    req_origin = request.META["Origin"] 
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if req_origin != host_server :
        return likedRequest(request.method,req_origin, AUTHOR_ID)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=AUTHOR_ID)
        except profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)
        liked = profile.liked
        serializer = LikedSerializer(liked)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

@csrf_exempt 
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET', 'DELETE'])
def inbox(request, AUTHOR_ID):
    # Inbox has a one-to-one relationship with User, and the User id is an integer, AUTHOR_ID
    # to avoid Reference problem , make a copy of AUTHOR_ID by creating a new string
    USER_ID = (AUTHOR_ID + '.')[:-1]
    req_origin = request.META["Origin"] 
    # Profile/AUTHOR ID is the full url
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    print("user id: ", USER_ID)

    if req_origin != host_server :
        return inboxRequest(request.method,req_origin, AUTHOR_ID)
    else:
        if request.method == "POST":
            user = User.objects.get(pk=USER_ID)
            data = JSONParser().parse(request)
            print("User: ", user)
            print("Data: ", data)
            if data['type'] == "post":
                print("Recieved a post inbox!")
                serializer = PostSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    post_id = data['id']
                    try:
                        post = Post.objects.get(id=post_id)
                    except:
                        serializer.save()
                        post = Post.objects.get(id=post_id)
                    user.inbox.post_inbox.items.add(post)
                    user.inbox.post_inbox.save()
                    user.profile.timeline.add(post)
                    user.profile.save()
                    return JsonResponse(data, status=200)
                return JsonResponse(serializer.errors, status=400) 
            elif data['type'] == 'like':
                print("Recieved a like inbox!")
                post_url = data['object'].split("/")
                # like post
                if len(port_url) == 7:
                    print("Post url: ", post_url)
                    user_id = post_url[-3]
                    print("User id: ", user_id)
                    post_id = post_url[-1]
                    print("Post id: ", post_id)
                    if user_id != AUTHOR_ID:
                        return JsonResponse({"Error": "Author id is inconsistent"}, status=404)
                    serializer = LikeSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        try:
                            post = Post.objects.get(id=post_id)
                        except:
                            return JsonResponse({"Error": "Post does not exist"}, status=404) 
                        like = serializer.save()
                        post.likes.add(like)
                        post.save()
                        user.inbox.like_inbox.add(like)
                        user.save()
                        return JsonResponse(data, status=200)
                    return JsonResponse(serializer.errors, status=400)
                #like comment
                elif len(post_url) == 9:
                    user_id = post_url[4]
                    post_id = post_url[6]
                    comment_id = post_url[8]
                    if user_id != AUTHOR_ID:
                        return JsonResponse({"Error": "Author id is inconsistent"}, status=404)
                    serializer = LikeSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        try:
                            comment = Comment.objects.get(id=comment_id)
                        except:
                            return JsonResponse({"Error": "comment does not exist"}, status=404) 
                        like = serializer.save()
                        comment.likes.add(like)
                        comment.save()
                        return JsonResponse(data, status=200)
                    return JsonResponse(serializer.errors, status=400)

            elif data['type'] == 'follow':
                print("Recieved a friend request!")
                serializer = FriendReuqestSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    friend_req = serializer.save()
                    user.inbox.friend_requests.add(friend_req)
                    user.inbox.save()
                    return JsonResponse(data, status=200)
                return JsonResponse(serializer.errors, status=400) 

            else:
                return JsonResponse({"Error": "Invalid inbox type"}, status=400) 

        elif request.method == "DELETE":
            user = User.objects.get(pk=USER_ID)
            user.inbox.post_inbox.items.clear()
            user.inbox.post_inbox.save()
            user.inbox.friend_requests.clear()
            user.inbox.like_inbox.clear()
            user.inbox.save()
            return JsonResponse({}, status=204)

        elif request.method == "GET":
            print("Get request processing...")
            user = User.objects.get(pk=USER_ID)
            print("User: ", user)
            post_inbox = user.inbox.post_inbox
            print("Post inbox: ", post_inbox)
            serializer = PostInboxSerializer(post_inbox)
            return JsonResponse(serializer.data, status=200)

