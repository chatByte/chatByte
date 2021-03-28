from django.http import JsonResponse
from .models import *
from .serializers import *
import requests

def profileRequest(method, origin, user_id, profile=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the author's profile in json format.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        serializer = ProfileSerializer(data=profile)
        if serializer.is_valid(raise_exception=True):
            response = requests.post(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
    return response

def postsRequest(method, origin, user_id, post=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the post to be created in json format.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/posts/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            response = requests.post(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
    return response

def postRequest(method, origin, user_id, post_id, post=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/<post id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET/DELETE request, otherwise, the body is
    the post in json format.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/posts/" + str(post_id) + "/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            response = requests.post(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
        response = requests.post(url, data=serializer.data, headers=headers)
    elif method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    elif method == "PUT":
        serializer = PostSerializer(data=post)
        if serializer.is_valid(raise_exception=True):
            response = requests.put(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
        response = requests.put(url, data=serializer.data, headers=headers)
    return response

def commentRequest(method, origin, user_id, post_id, comment=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/<post id>/comments/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the comment in json format.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/posts/" + str(post_id) + "/comments/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        serializer = CommentSerializer(data=comment)
        if serializer.is_valid(raise_exception=True):
            response = requests.post(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
        response = requests.post(url, data=serializer.data, headers=headers)
        return response
    return response

def inboxRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/inbox/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET/DELETE request, otherwise, the body is
    the inbox in json format.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/inbox/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        if data['type'] == "post":
            print("Recieved a post inbox!")
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                response = requests.post(url, data=serializer.data, headers=headers)
            else:
                response =  JsonResponse(serializer.errors, status=400)
        elif data['type'] == 'like':
            serializer = LikeSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                response = requests.post(url, data=serializer.data, headers=headers)
            else:
                response =  JsonResponse(serializer.errors, status=400) 
        elif data['type'] == 'follow':
            print("Recieved a friend request!")
            serializer = FriendReuqestSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                response = requests.post(url, data=serializer.data, headers=headers)
            else:
                response =  JsonResponse(serializer.errors, status=400)
        else:
            return JsonResponse({"Error": "Invalid inbox type"}, status=400) 
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    elif method == "GET":
        print("Get request processing...")
        response = requests.get(url, headers=headers)
    return response

def followersRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/followers/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/followers/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers)
    return response

def followerRequest(method, origin, user_id, foreign_author_id,data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/followers/<foreign author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''
    url = str(origin) + "/author/" + str(user_id) + "/" + str(foreign_author_id) + "/"
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        serializer = FollowerSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            response = requests.post(url, data=serializer.data, headers=headers)
        else:
            response =  JsonResponse(serializer.errors, status=400)
        return response
    return response