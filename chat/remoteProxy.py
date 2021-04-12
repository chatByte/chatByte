from django.http import JsonResponse
from .models import *
from .serializers import *
import requests
from .signals import host
from requests.auth import HTTPBasicAuth
from django.contrib.auth.models import User
import json

def profileRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the author's profile in json format.
    '''
    if origin == "https://hermes-cmput404.herokuapp.com/":
        url = str(origin) + "api/author/" + str(user_id)
    else:
        url = str(origin) + "author/" + str(user_id)
    print("Remote get profile origin: ", origin)
    user = User.objects.get(last_name=origin)
    headers = {
        'Origin': host,
        'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
    elif method == "POST":
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
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
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
    elif method == "POST":
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
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
    url = str(origin) + "author/" + str(user_id) + "/posts/" + str(post_id)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "PUT":
        response = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    return response

def commentRequest(method, origin, user_id, post_id, local_user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/posts/<post id>/comments/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET request, otherwise, the body is
    the comment in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/posts/" + str(post_id) + "/comments"
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(local_user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
    elif method == "POST":
        print("commentRequest():", url)
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
        # print(response.body)
    return response

def inboxRequest(method, origin, user_id, data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/inbox/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty if it is a GET/DELETE request, otherwise, the body is
    the inbox in json format.
    '''
    url = str(origin) + "author/" + str(user_id) + "/inbox"
    like_url = str(origin) + "author/" + str(user_id) + "/likes"
    print("remote URL: ", url)
    print("remote origin: ", origin)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "POST":
        headers['Content-type'] = 'application/json'
        if data['type'] == "post":
            print("Recieved a post inbox!")
            print("Username: ", user.username, "first_name: ", user.first_name)
            print(json.dumps(data))
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
            print(response.status_code)
        elif data['type'].lower() == 'like':
            response = requests.post(like_url, data=json.dumps(data['data']), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
            print(response.status_code)
        elif data['type'].lower() == 'follow':
            print("Recieved a friend request!")
            response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
            print(response.status_code)
        else:
            return JsonResponse({"Error": "Invalid inbox type"}, status=400) 
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "GET":
        print("Get request processing...")
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
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
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    return response

def followerRequest(method, origin, user_id, foreign_author_id,data=None):
    '''
    This function send a request to the remote server at:
        service/author/<author id>/followers/<foreign author id>/
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''
    url = str(origin) + "author/" + str(user_id) + "/followers/" + str(foreign_author_id)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=405) 
    print("url", url)
    print("Method: ", method)
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    elif method == "PUT":
        response = requests.put(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
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
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    return response

def likesRequest(method, origin, user_id, post_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/likes/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/posts/" + post_id + "/likes"
    print("get post likes url: ", url)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    return response

def commentLikesRequest(method, origin, user_id, post_id, comment_id, data=None):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/likes/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/posts/" + post_id + "/comments/" + comment_id + "/likes"
    print("get comment likes url: ", url)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
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
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    if method == "GET":
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
        print(response.status_code)
    return response

def streamRequest(origin, user_id):
    '''
    This function send a request to the remote server at:
        "author/<str:AUTHOR_ID>/stream/"
    with the corresponding method. Headers are included to ensure secure connections.
    The body of the request is empty.
    '''

    url = str(origin) + "author/" + str(user_id) + "/stream/?page=1&size=1000"
    print(url)
    user = User.objects.get(last_name=origin)
    headers = {'Origin': host, 'X-Request-User': str(host) + "author/" + str(user_id)}
    response = JsonResponse({"Error": "Bad request"}, status=400) 
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(user.username, user.first_name))
    print(response.status_code)
    return response