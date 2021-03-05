from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author
from .models import Post

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse


from .form import *

from .api import *

from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.http import JsonResponse
from django.forms.models import model_to_dict

"""
views.py receive request and create repose to client,
Create your views here.
"""

# default value
cur_user_name = "teemo"


def login(request):
    global cur_user_name
    context = {}
    context['form']= LoginForm()
    if request.method == "GET":
        return render(request, "chat/login.html", context)
    elif request.method == "POST":
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        print(username, password)
        valid = validActor(username, password)
        if valid:
            cur_user_name = username
            return redirect("/chat/home")
        else:
            messages.error(request, "Invalid user name or password!")

            return render(request, 'chat/login.html', context)
   

# # Create your views here.
# def home_view(request):
#     context ={}
#     context['form'] = InputForm()
#     return render(request, "chat/signup.html", context)

def signup(request):
    global cur_user_name
    context = {}
    context['form'] = CreateAuthorForm()
    if request.method == "GET":
        return render(request, "chat/signup.html", context)
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("GitHub")
        password = request.POST.get("Password")
        retype_password = request.POST.get("Retype_password")
        host = request.POST.get("Host")
        if getAuthor(username) != None:
            messages.error(request, 'User name exists!')
            return render(request, "chat/signup.html", context)
        else:
            if retype_password != password:
                messages.error(request, 'Password does not match!')
                return render(request, "chat/signup.html", context)
            print(createActor(username, password))
            createAuthor(host, username, url, github)
            cur_user_name = username
            return redirect("/chat/home/")
        # if createAuthor("this", username, url, github):
        #   return redirect("/chat/profile/")
        # else:
        #   messages.error(request, 'User name exists!')
        #   return render(request, "chat/signup.html", context)

def home(request):
    global cur_user_name
    cur_author = getAuthor(cur_user_name)
    # a list of post
    # mytimeline = getTimeline(cur_user_name)
    mytimeline = getTimeline(cur_user_name)
    dynamic_contain = {
        'myName' : cur_author.DISPLAY_NAME,
        'timeline': mytimeline

    }

    # query to database
    # timeline =

    if request.method == "GET":

        # print ("Request URL Path = [" + request.path() + "], ")
        # getTimeline()
        return render(request, "chat/home.html", dynamic_contain)
    elif request.method == "POST":

        # change later
        return render(request, "chat/home.html", dynamic_contain)



def friend_profile(request):
    timeline = {}
    # query to database

    # timeline = 
    return render(request, "chat/friendProfile.html", timeline)



def make_post(request):
    # post = {}

    # hard coding ??
    cur_author = getAuthor(cur_user_name)
    # ??
    # cur_user_name = cur_author.DISPLAY_NAME # or we can use global
    # testcase
    dynamic_contain = {
        'fullName':'Ritsu Onodera',

        'test_name': cur_user_name
    }
    dynamic_contain['form'] = CreatePostForm()

    # Get the current pages' author

    if request.method == "GET":

        return render(request, "chat/feed.html", dynamic_contain)

    elif request.method == "POST":

        request_post = request.POST

        info = request_post.get("description", "")

        title = request_post.get("title", "")
        source = cur_user_name # Who share it to me
        origin = cur_user_name # who origin create
        description = request_post.get("description", "")
        content_type = "Latin"
        content = info
        author = cur_author
        categories = "text" # web, tutorial, can be delete  # ?? dropdown
        visibility = "" # direct get id name form web

        createFlag = createPost(title, source, origin, description, content_type, content, author, categories, visibility)
        if createFlag:
            print("haha, successful create post, info: ", info)

        else:
            print("sever feels sad ", info)

        return render(request, "chat/feed.html", dynamic_contain)



    # # get post
    # return render(request, "chat/feed.html", dynamic_contain)

def profile(request):
    global cur_user_name
    author = getAuthor(cur_user_name)
    actor = getActor(cur_user_name)
    print(author)
    # context = model_to_dict(author)
    form = ProfileForm()
    form.fields['User_name'].initial = author.DISPLAY_NAME
    form.fields['Host'].initial = author.HOST
    form.fields['Url'].initial = author.URL
    form.fields['GitHub'].initial = author.GITHUB
    form.fields['Password'].initial = actor.PASSWORD
    context = {}
    context['form']= form
    print(context)
    # query to database
    if request.method == "GET":
        return render(request, "chat/myProfile.html", context)
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("GitHub")
        password = request.POST.get("Password")
        host = request.POST.get("Host")
        print("update author: ", updateAuthor(username, host, url, github, password))
        print("update actor: ", updateActor(username, password))
        cur_user_name = username
        return render(request, "chat/myProfile.html", context)
