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
        try:
            post = Post.objects.get(id=POST_ID)
            return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' already exists'}, status=404)
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
            profile = Profile.objects.get(pk=AUTHOR_ID)
            serializer.save(author=profile)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




# coment views.py
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_obj(request, AUTHOR_ID, POST_ID):
    comments = Comment.objects.all()
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username

    if request.method == 'GET':
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)


    # if request.method == "GET":
    #     comments = getComments(POST_ID)

    #     # TODO return objects or html?
    #     return comments
    # elif request.method == "POST":
    #     request_post = request.POST
    #     author = request_post.get("author")
    #     contentType = request_post.get("contentType")
    #     comment = request_post.get("comment")
    #     createComment(author, comment, contentType)
    #     return request_post

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




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
def delete_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True

def add_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True




