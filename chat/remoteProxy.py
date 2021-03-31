from django.http import JsonResponse
from .models import *
from .serializers import *
import requests
from .signals import host
from requests.auth import HTTPBasicAuth
from django.contrib.auth.models import User

def profileRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the author's profile in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/"
    user = User.objects.get(last_name=origin)
    headers = {
        'Origin': host,
        'X-Request-User': str(host) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
    elif method == "POST":
        response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def postsRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the post to be created in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/posts/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
    elif method == "POST":
        response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def postRequest(method, origin, user_id, post_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/<post id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET/DELETE request, otherwise, the body is
    the post in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/posts/" + str(post_id) + "/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    elif method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    elif method == "PUT":
        response = requests.put(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def commentRequest(method, origin, user_id, post_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/<post id>/comments/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the comment in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/posts/" + str(post_id) + "/comments/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
    elif method == "POST":
        response = requests.post(url, data=serializer.data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def inboxRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/inbox/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET/DELETE request, otherwise, the body is
    the inbox in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/inbox/"
    print("remote URL: ", url)
    print("remote origin: ", origin)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        if data['type'] == "post":
            print("Recieved a post inbox!")
            response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
            print(response.status_code)
        elif data['type'] == 'like':
            response = requests.post(url, data=data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
            print(response.status_code)
        elif data['type'] == 'follow':
            print("Recieved a friend request!")
            response = requests.post(url, data=serializer.data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
            print(response.status_code)
        else:
            return JsonResponse({"Error": "Invalid inbox type"}, status=400) 
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    elif method == "GET":
        print("Get request processing...")
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def followersRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/followers/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''
    url = str(origin) + "author/" + str(user_id) + "/followers/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def followerRequest(method, origin, user_id, foreign_author_id,data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/followers/<foreign author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''
    url = str(origin) + "author/" + str(user_id) + "/" + str(foreign_author_id) + "/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    elif method == "POST":
        response = requests.post(url, data=serializer.data, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response


def likedRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/liked/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/liked/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def likesRequest(method, origin, user_id, post_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/likes/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/posts/" + post_id + "/likes/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def commentLikesRequest(method, origin, user_id, post_id, comment_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/likes/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/posts/" + post_id + "/comments/" + comment_id + "/likes/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response

def friendsRequest(method, origin, user_id, post_id, comment_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/likes/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/friends/"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': origin, 'X-Request-User': str(origin) + "author/" + str(user_id) + "/"}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.password))
        print(response.status_code)
    return response