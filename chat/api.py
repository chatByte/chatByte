from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes

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
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def post_obj(request, AUTHOR_ID, POST_ID):
    print("?????")
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]

    try:
        post = Post.objects.get(ID=POST_ID)
    except Post.DoesNotExist:
        return HttpResponse(status=404)


    if request.method == "DELETE":
        deletePost(POST_ID)
        response = redirect("../my_posts/")
        return HttpResponse(status=204)
    elif request.method == "GET":
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required
@require_http_methods(["GET"])
def posts_obj(request, AUTHOR_ID):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)

        return JsonResponse(serializer.data, safe = False)



# coment views.py
@require_http_methods(["GET", "POST"])
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
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@require_http_methods(["GET", "POST"])
def profile_obj(request, AUTHOR_ID):
    profile = Profile.objects.get(pk=AUTHOR_ID)
    try:
        profile = Profile.objects.get(user_id=AUTHOR_ID)
    except profile.DoesNotExist:
        return HttpResponse(status=404)

    # query to database
    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        # post_obj = json.loads(request.body)
        # url = post_obj["url"]
        # displayName = post_obj["displayName"]
        # github = post_obj["github"]
        # # we do not allowed leave our server
        # # host = post_obj["host"]
        # updateProfile(displayName, url, github)
        # return post_obj




@require_http_methods(["GET"])
def delete_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True

def add_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True




