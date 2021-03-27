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

@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def post_obj(request, AUTHOR_ID, POST_ID):
    # cur_user_name = None
    # if request.user.is_authenticated:
    #     cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]
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
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def posts_obj(request, AUTHOR_ID):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
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
'''
Get conmments  for a Post
Response Object Structure: [list of Like objects] using json
'''
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_obj(request, AUTHOR_ID, POST_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username


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

    elif request.method == "DELETE":
        # TODO
        pass
        
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

"""
REST Author, Generate response at my profile page ,
"""
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile_obj(request, AUTHOR_ID):
    profile = Profile.objects.get(pk=AUTHOR_ID)
    try:
        profile = Profile.objects.get(user_id=AUTHOR_ID)
    except profile.DoesNotExist:
        return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)

    # query to database
    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(profile, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED,)
        return JsonResponse(serializer.errors, status=400)
        # post_obj = json.loads(request.body)
        # url = post_obj["url"]
        # displayName = post_obj["displayName"]
        # github = post_obj["github"]
        # # we do not allowed leave our server
        # # host = post_obj["host"]
        # updateProfile(displayName, url, github)
        # return post_obj




@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True




@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True







'''
Get likes for a Post
Response Object Structure: [list of Like objects]
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'PUT'])
def likes_post_obj(request, AUTHOR_ID, POST_ID):
    #TODO
    # comments = Comment.objects.all()
    # cur_user_name = None
    # if request.user.is_authenticated:
    #     cur_user_name = request.user.username

    # if request.method == 'GET':
    #     serializer = CommentSerializer(comments, many=True)
    #     return JsonResponse(serializer.data, safe=False)

    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     serializer = CommentSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=201)
    #     return JsonResponse(serializer.errors, status=400)




    return True



@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_post_obj(request, AUTHOR_ID):
    #TODO
    return True
