from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author
from .models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.http import JsonResponse

from .form import *
from .api import *
import base64
import os
"""
views.py receive request and create repose to client,
Create your views here.
"""


"""
Generate response at login page  
"""
def login(request):
    cur_user_name = request.COOKIES.get('user')
    context = {}
    context['form']= LoginForm()
    if request.method == "GET":
        return render(request, "chat/login.html", context)
    elif request.method == "POST":
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        valid = validActor(username, password)
        if valid:
            cur_user_name = username
            response = redirect("/chat/home")
            setCookie(response, 'user', cur_user_name)
            return response
        else:
            messages.error(request, "Invalid user name or password!")
            response = render(request, 'chat/login.html', context)
            setCookie(response, 'user', cur_user_name)
            return response

"""
Generate response at signup page  
"""

def signup(request):
    cur_user_name = request.COOKIES.get('user')
    context = {}
    context['form'] = CreateAuthorForm()
    response = render(request, "chat/signup.html", context)
    setCookie(response, 'user', cur_user_name)
    if request.method == "GET":
        return response
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("GitHub")
        password = request.POST.get("Password")
        retype_password = request.POST.get("Retype_password")
        host = request.POST.get("Host")
        # first method to handle user name exist, can be optimize later
        if validActor(username, password):
            messages.error(request, 'User name exists!')
            return response
        else:
            if retype_password != password:
                messages.error(request, 'Password does not match!')
                return response
            createAuthor(host, username, url, github)
            createActor(username, password)
            cur_user_name = username
            response = redirect("/chat/home/")
            setCookie(response, 'user', cur_user_name)
            return response
        # second method to handle user name exist, can be optimize later
        # if createAuthor("this", username, url, github):
        #   return redirect("/chat/profile/")
        # else:
        #   messages.error(request, 'User name exists!')
        #   return render(request, "chat/signup.html", context)


"""
Generate response at home page  
"""
def home(request):
    cur_user_name = request.COOKIES.get('user')
    cur_author = getAuthor(cur_user_name)
    # a list of post
    mytimeline = getTimeline(cur_user_name)

    author_num_follwers = len(cur_author.FOLLOWERS.all())

    dynamic_contain = {
        'myName' : cur_author.DISPLAY_NAME,
        'timeline': mytimeline,
        'author_num_follwers': author_num_follwers

    }


    response = render(request, "chat/home.html", dynamic_contain)
    setCookie(response, 'user', cur_user_name)

    # query to database

    if request.method == "GET":

        return response
    elif request.method == "POST":

        # change later
        return response


"""
Generate response at friend_profile page , Now is deafault friend Zoe, need to be handled later 
"""
def friend_profile(request):
    cur_user_name = request.COOKIES.get('user')
    timeline = {}

    response = render(request, "chat/friendProfile.html", timeline)
    setCookie(response, 'user', cur_user_name)
    return response



"""
Generate response at feed page ,
"""
def make_post(request):
    cur_user_name = request.COOKIES.get('user')
    """
    so far, only support text-only post and post with img and caption
    Prob: 1. createPost return error!
    """
    cur_author = getAuthor(cur_user_name)
    mytimeline = getTimeline(cur_user_name)
    author_num_follwers = 10

    dynamic_contain = {
        'fullName':'Ritsu Onodera',
        'author_num_follwers': author_num_follwers,
        'test_name': cur_user_name,
        'myName' : cur_author.DISPLAY_NAME,
        'timeline': mytimeline

    }

    # Get the current pages' author

    if request.method == "GET":
        response = render(request, "chat/feed.html", dynamic_contain)
        setCookie(response, 'user', cur_user_name)
        return response

    elif request.method == "POST":

        request_post = request.POST
        title = request_post.get("title", "")
        source = cur_user_name # Who share it to me
        origin = cur_user_name # who origin create
        description = request_post.get("description", "")
        content_type = request_post.get("contentType", "")
        f = request.FILES.get("file", "")
        author = cur_author
        categories = "text/plain" # web, tutorial, can be delete  # ?? dropdown
        visibility = request_post.get("visibility", "")

        if len(f) > 0:
            categories = "image/" + os.path.splitext(f.name)[-1][1:]
            with f.open("rb") as image_file:
                content = base64.b64encode(image_file.read())
        else:
            content = description

        createFlag = createPost(title, source, origin, description, content_type, content, author, categories, visibility)
        if createFlag:
            print("haha, successful create post, info: ", description)
            response = redirect("/chat/home/")
            setCookie(response, 'user', cur_user_name)
            return response
        else:
            print("sever feels sad ", description)

        response = render(request, "chat/feed.html", dynamic_contain)
        setCookie(response, 'user', cur_user_name)
        return response



"""
Generate response at my profile page , 
"""
def profile(request):
    cur_user_name = request.COOKIES.get('user')
    author = getAuthor(cur_user_name)
    actor = getActor(cur_user_name)
    form = ProfileForm()
    form.fields['User_name'].initial = author.DISPLAY_NAME
    form.fields['Host'].initial = author.HOST
    form.fields['Url'].initial = author.URL
    form.fields['GitHub'].initial = author.GITHUB
    form.fields['Password'].initial = actor.PASSWORD
    context = {}
    context['form']= form
    context['myName']= author.DISPLAY_NAME

    # query to database
    if request.method == "GET":
        response = render(request, "chat/myProfile.html", context)
        setCookie(response, 'user', cur_user_name)
        return response
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("GitHub")
        password = request.POST.get("Password")
        host = request.POST.get("Host")
        updateAuthor(username, host, url, github)
        updateActor(username, password)
        cur_user_name = username
        response = render(request, "chat/myProfile.html", context)
        setCookie(response, 'user', cur_user_name)
        return response


"""
Generate response ,when delete user at home  page , 
"""
def delete(request, ID):
    cur_user_name = request.COOKIES.get('user')
    # post_id = request.build_absolute_uri().split("/")[-2][6:]
    cur_author = getAuthor(cur_user_name)
    deletePost(ID)
    response = redirect("/chat/home/")
    setCookie(response, 'user', cur_user_name)
    return response


"""
Generate response ,when delete user at feed page , 
"""
def delete_in_feed(request, ID):
    cur_user_name = request.COOKIES.get('user')
    # post_id = request.build_absolute_uri().split("/")[-2][6:]
    cur_author = getAuthor(cur_user_name)
    deletePost(ID)
    response = redirect("/chat/feed/")
    setCookie(response, 'user', cur_user_name)
    return response

def edit(request, ID):
    print(request.POST)
    new_description = request.POST.get("editText")
    print(new_description)
    editPostDescription(ID, new_description)
    response = redirect("/chat/feed/")
    return response

def edit_in_feed(request, ID):
    print(request.POST)
    new_description = request.POST.get("editText")
    print(new_description)
    print(editPostDescription(ID, new_description))
    response = redirect("/chat/feed/")

    return response
