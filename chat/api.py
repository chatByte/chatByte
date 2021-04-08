from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
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
import json

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
    USER_ID = (AUTHOR_ID + '.')[:-1]
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    USER_POST_ID = POST_ID
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID

    print("post id: ", POST_ID)
    print(request.META)
    server_origin = request.META.get("HTTP_X_SERVER")
    print(server_origin)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return postRequest(request.method,server_origin, USER_ID, USER_POST_ID, request.data)
    else:
        if request.method == "DELETE":
            # remove the post
            try:
                Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                print("here post does not exist")
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
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return postsRequest(request.method,server_origin, USER_ID, request.data)
    else:
        if request.method == 'GET':
            profile = Profile.objects.get(id=AUTHOR_ID)
            posts = profile.timeline
            print(posts.all())
            # serializer = PostSerializer(posts, many=True)
            # pagination
            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(posts.all(), request)

            serializer = PostSerializer(paginated_results, many=True)

            data = {
                'count': pagination.page.paginator.count,
                'next': pagination.get_next_link(),
                'previous': pagination.get_previous_link(),
                'posts': serializer.data,
            }
            return JsonResponse(data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                profile = Profile.objects.get(id=AUTHOR_ID)
                post = serializer.save(author=profile)
                print(post)
                profile.timeline.add(post)
                profile.save()
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
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    USER_POST_ID = POST_ID
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return commentRequest(request.method,server_origin, USER_ID, USER_POST_ID, request.data)
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

            # pagination
            # pagination
            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(comments.all(), request)

            serializer = CommentSerializer(paginated_results, many=True)

            data = {
                'count': pagination.page.paginator.count,
                'next': pagination.get_next_link(),
                'previous': pagination.get_previous_link(),
                'results': serializer.data,
            }
            return JsonResponse(data, safe=False)

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
                profile = Profile.objects.get(id=AUTHOR_ID)

                if (createComment(profile, POST_ID, data["comment"], data["contentType"], data["published"])):

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
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    print("Origin: ", host_server)
    print("Request origin: ", server_origin)
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return profileRequest(request.method,server_origin, USER_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        # query to database
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return JsonResponse(serializer.data, status=201)
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
    # req_origin = request.META["Origin"]
# <<<<<<< HEAD
#     # print(request.META)
#     server_origin = request.META["HTTP_X_SERVER"]
#     print(server_origin)
#     AUTHOR_ID = host_server + "author/" + AUTHOR_ID
#     print("author id: ", AUTHOR_ID)

# =======
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    FOREIGN_USER_ID = FOREIGN_AUTHOR_ID
    print("follower's id: ", FOREIGN_AUTHOR_ID)


    try:
        FOREIGN_AUTHOR_ID = server_origin + "author/" + FOREIGN_AUTHOR_ID
    except:
        FOREIGN_AUTHOR_ID = host_server + "author/" + FOREIGN_AUTHOR_ID
    print("post id: ", FOREIGN_AUTHOR_ID)
    print("server_origin", server_origin)
    print("host_server", host_server)


    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return followerRequest(request.method,server_origin, USER_ID, FOREIGN_USER_ID, request.data)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=USER_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)


        if (request.method == "GET"):
            # reponse a status
            # check if follower
            try:
                print("Searching foreign author id: ", FOREIGN_AUTHOR_ID)
                try:
                    follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)
                except:
                    return JsonResponse({'status':'false','message':'FOREIGN_AUTHOR_ID: ' + FOREIGN_AUTHOR_ID + ' does not exists'}, status=404)
                if follower in profile.followers.items.all():
                    serializer = ProfileSerializer(follower)
                    return JsonResponse({'detail':'true'}, status=200)
                else:
                    return JsonResponse({'detail':'false'}, status=200)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'FOREIGN_AUTHOR_ID: ' + FOREIGN_AUTHOR_ID + ' does not exists'}, status=404)

        elif (request.method == "PUT"):
            #add a follower , with FOREIGN_AUTHOR_ID
            data = JSONParser().parse(request)
            serializer = ProfileSerializer(data=data)
            try:
                follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)
                profile.followers.items.add(follower)
                return JsonResponse({'detail': 'true'}, status=201)

            except Profile.DoesNotExist:
                if serializer.is_valid(raise_exception=True):
                    follower_profile = serializer.save()
                    profile = Profile.objects.get(id=AUTHOR_ID)
                    # follower = serializer.data
                    profile.followers.items.add(follower_profile)
                    profile.save()
                return JsonResponse(serializer.data, status=201)
            # return JsonResponse(serializer.errors, status=400)

        elif request.method == "DELETE":
            follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)
            profile.followers.items.remove(follower)
            return JsonResponse({"status": "true"}, status=200)

        return JsonResponse({"Error": "Bad request"}, status=400)




'''
# URL: ://service/author/{AUTHOR_ID}/followers/
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def followers_obj(request, AUTHOR_ID):
    # ex. equest.META[origin] == ("https:\\chatbyte"):
    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return followersRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        followers = profile.followers.items.all()
        serializer = ProfileSerializer(followers, many=True)
        if request.method == "GET":
            return JsonResponse({"type": "followers", "items": serializer.data}, status=200, safe=False)

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
    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return friendsRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        friends = profile.friends
        serializer = ProfileSerializer(friends, many=True)
        if request.method == "GET":
            return JsonResponse({"type": "friends", "items": serializer.data}, status=200, safe=False)

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
    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return likesRequest(request.method, server_origin, AUTHOR_ID, POST_ID, request.data)
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
    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    print("post id: ", POST_ID)
    COMMENT_ID = POST_ID + "/comments/" + COMMENT_ID
    print("comment id: ", COMMENT_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return likesRequest(request.method, server_origin, AUTHOR_ID, POST_ID, COMMENT_ID, request.data)
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

    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return likedRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)
        liked = profile.liked
        serializer = LikedSerializer(liked)
        if serializer.is_valid(raise_exception=True):
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)


'''
# Inbox has a one-to-one relationship with User, and the User id is an integer, AUTHOR_ID
# to avoid Reference problem , make a copy of AUTHOR_ID by creating a new string

URL: ://service/author/{AUTHOR_ID}/inbox
GET: if authenticated get a list of posts sent to {AUTHOR_ID}
POST: send a post to the author
    if the type is “post” then add that post to the author’s inbox
    Here folllow is equal to be a friend request
    if the type is “follow” then add that follow is added to the author’s inbox to approve later
    if the type is “like” then add that like to the author’s inbox
DELETE: clear the inbox
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET', 'DELETE'])
def inbox(request, AUTHOR_ID):
    # print("inbox: ", request)
    USER_ID = (AUTHOR_ID + '.')[:-1]

    # add for test purpose
    if not request.META.get("HTTP_X_SERVER"):
        server_origin = host_server
    #
    else:
        # req_origin = request.META["Origin"]
        server_origin = request.META.get("HTTP_X_SERVER")
    # Profile/AUTHOR ID is the full url
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("Origin header: ", origin_server)
    print("author id: ", AUTHOR_ID)
    print("user id: ", USER_ID)

    if server_origin is not None and server_origin != host_server:
        print("------ Remote request body: ", request.data)
        return inboxRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        print("Request: ", request)
        # print("Request data: ", request.data)
        # print("Request body: ", request.body)
        if request.method == "POST":
            print("Using post method")
            user = User.objects.get(pk=USER_ID)
            # print(request.data)
            print("User", user)
            try:
                # data = JSONParser().parse(request.data)
                data = json.loads(request.data)
            except BaseException as e:
                print("error parsing request's body")
                return JsonResponse({e}, status=400, safe=False)
            # data = request.data
            # data = json.loads(request.body.decode('utf-8'))
            print("User: ", user)
            print("Data: ", data)
            if data['type'] == "post":
                print("Recieved a post inbox...!")
                serializer = PostSerializer(data=data)
                # print(serializer)
                if serializer.is_valid(raise_exception=True):
                    print("Post id: ", data['id'])
                    post_id = data['id']
                    try:
                        post = Post.objects.get(id=post_id)
                    except Post.DoesNotExist:
                        author_dict = data['author']
                        print("Author dict: ", author_dict)
                        try:
                            author = Profile.objects.get(id=author_dict['id'])
                        except Profile.DoesNotExist:
                            author_serializer = ProfileSerializer(data=author_dict)
                            if author_serializer.is_valid(raise_exception=True):
                                author = author_serializer.save()
                        post = serializer.save(author=author)
                    print("Post: ", post)
                    post = Post.objects.get(id=post_id)
                    user.inbox.post_inbox.items.add(post)
                    user.inbox.post_inbox.save()
                    user.profile.timeline.add(post)
                    user.profile.save()
                    return JsonResponse(data, status=200)
                else:
                    print("here")
                    return JsonResponse(serializer.errors, status=400)
            elif data['type'] == 'like':
                print("Recieved a like inbox!")
                post_url = data['object'].split("/")
                # like post
                if len(post_url) == 7:
                    print("Post url: ", post_url)
                    user_id = post_url[-3]
                    print("User id: ", user_id)
                    # post_id = post_url[-1]
                    post_id = host_server + 'author/' + USER_ID + '/posts/' + post_url[-1]
                    print("Post id: ", post_id)
                    if user_id != USER_ID:
                    # if user_id != AUTHOR_ID: # Now AUTHOR_ID is http://our-host-name/USER_ID
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
                    # post_id = post_url[6]
                    post_id = host_server + 'author/' + user_id + '/posts/' + post_url[6]

                    # comment_id = post_url[8]
                    comment_id = host_server + 'author/' + user_id + '/posts/' + post_url[6] + '/comments/' + post_url[8]

                    # if user_id != AUTHOR_ID:
                    if user_id != USER_ID:
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
                print(data['actor'])
                print(data['object'])
                print(data['summary'])

                serializer = FriendReuqestSerializer(data=data)
                if serializer.is_valid(raise_exception=True):

                    actor_dict = data['actor'] 

                    try:
                        actor = Profile.objects.get(id=actor_dict['id'])
                    except Profile.DoesNotExist:
                        actor_serializer = ProfileSerializer(data=actor_dict)
                        if actor_serializer.is_valid(raise_exception=True):
                            actor = actor_serializer.save()

                    object_dict = data['object'] 

                    try:
                        object = Profile.objects.get(id=object_dict['id'])
                    except Profile.DoesNotExist:
                        object_serializer = ProfileSerializer(data=object_dict)
                        if object_serializer.is_valid(raise_exception=True):
                            object = object_serializer.save()
                    friend_req = serializer.save(actor=actor, object=object)

                    #friend_req = serializer.save()


                    # -----------------
                    # add to object's inbox
                    # TODO: handle remote object

                    object.user.inbox.friend_requests.add(friend_req)
                    # -----------------



                    # user.inbox.friend_requests.add(friend_req)
                    #print("friend req: ", friend_req)

                    # should not be id, should be obj 
                    # print(friend_req.dict)

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

@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def stream_obj(request, AUTHOR_ID):

    # req_origin = request.META["Origin"]
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    print("author id: ", AUTHOR_ID)
    print("Origin header: ", origin_server)

    if server_origin is not None and server_origin != host_server:
        print("Remote request body: ", request.data)
        return likedRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        if request.method == 'GET':
            try:
                print("here")
                try:
                    profile = Profile.objects.get(id=AUTHOR_ID)
                    print(profile)
                except Profile.DoesNotExist:
                    print("profile not found!")
                posts_result = Post.objects.filter(visibility='public')
                print(posts_result)
                # all_author_posts = Post.objects.filter(author=profile)
                # print(all_author_posts)
                # all_following = Follower.objects.filter(items__id=profile)
                # print(all_following)
                # posts_result = all_author_posts
                # print("Result: ", posts_result)
                # for following in all_following:
                #     posts_result = posts_result | following.timeline.filter(visibility='public')
            except BaseException as e:
                print(e)
                posts_result = []
            # Get posts that's visible to the author
            print("Post result:", posts_result)

            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(posts_result, request)

            serializer = PostSerializer(paginated_results, many=True)

            data = {
                'count': pagination.page.paginator.count,
                'next': "", # pagination.get_next_link(),
                'previous': "", # pagination.get_previous_link(),
                'posts': serializer.data,
            }
            return JsonResponse(data, safe=False)
