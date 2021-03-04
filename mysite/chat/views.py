from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author
from .models import Post

from .form import InputForm, CreateAuthorForm
from .api import *

from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.http import JsonResponse

"""
views.py receive request and create repose to client, 
Create your views here.
"""

# default value
cur_user_name = "teemo" 


def home(request):

    context = {}
    context['form']= InputForm()
    if request.method == "GET":
        return render(request, "chat/home.html", context)
    elif request.method == "POST":
        username = request.POST.get("User_name")
        password = request.POST.get("Password")
        valid = validUser(username, password)
        if valid:
            cur_user_name = username
            return redirect("/chat/profile")
        else:
            messages.error(request, "Invalid user name or password!")
            return render(request, 'chat/home.html', context)
   
# # Create your views here.
# def home_view(request):
#     context ={}
#     context['form'] = InputForm()
#     return render(request, "chat/signup.html", context)

def signup(request):
    context = {}
    context['form'] = CreateAuthorForm()
    if request.method == "GET":
        return render(request, "chat/signup.html", context)
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("Github")
        password = request.POST.get("Password")
        if getAuthor(username) != None:
            messages.error(request, 'User name exists!')
            return render(request, "chat/signup.html", context)
        else:
            print(createUser(username, password))
            createAuthor("this", username, url, github)
            return redirect("/chat/profile/")
        # if createAuthor("this", username, url, github):
        #   return redirect("/chat/profile/")
        # else:
        #   messages.error(request, 'User name exists!')
        #   return render(request, "chat/signup.html", context)

def my_timeline(request):


    cur_author = getAuthor(cur_user_name)
    # a list of post
    # mytimeline = getTimeline(cur_user_name)
    mytimeline = cur_author.TIMELINE


    dynamic_contain = {

        'fullName': cur_author.DISPLAY_NAME,
        'timeline': mytimeline
        
    }
    print("_____")
    print (cur_author.DISPLAY_NAME)
    print (cur_author)
    print (cur_author.TIMELINE)

    print("mytimeline" , mytimeline)
    # query to database
    # timeline = 

    if request.method == "GET":



        print ("Request URL Path = [" + request.path() + "], ")

        # getTimeline()
        return render(request, "chat/timeline1.html", dynamic_contain)

    elif request.method == "POST":

        # change later
        return render(request, "chat/timeline1.html", dynamic_contain)



def others_timeline(request):
    timeline = {}
    # query to database
    # timeline = 
    return render(request, "chat/timeline2.html", timeline)

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
    # Get the current pages' author

    if request.method == "GET":

        return render(request, "chat/feed.html", dynamic_contain)

    elif request.method == "POST":

        request_post = request.POST
        info = request.POST.get("post_content", "")
        # print("---------/n",request_post)

        title = "Noli flere" # ??
        source = cur_user_name # Who share it to me
        origin = cur_user_name # who origin create 
        description = "Noli flere" # post about wt, high abstract
        content_type = "Latin" # texts, markdown imgs # ?? dropdown
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
    author = {}


    # query to database
    return render(request, "chat/profile.html", author)