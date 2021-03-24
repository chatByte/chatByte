from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db import transaction

from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .form import *
from .api import *
import base64
import os
import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

"""
views.py receive request and create repose to client,
Create your views here.
"""

# #class based view
# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'


"""
Generate response at login page  
"""
# def login(request):
#     context = {}
#     context['form']= UserForm()
#     if request.method == "GET":
#         return render(request, "chat/login.html", context)
#     elif request.method == "POST":
#         username = None
#         if request.user.is_authenticated:
#             username = request.user.username
#             cur_user_name = username
#             response = redirect("/chat/home")
#             return response
#         else:
#             messages.error(request, "Invalid user name or password!")
#             response = render(request, 'chat/login.html', context)
#             return response

# """
# Generate response at signup page  
# # """
# def signup(request):
#     context = {}
#     context['UserForm'] = UserForm()
#     context['ProfileForm'] = ProfileForm()
#     response = render(request, "chat/signup.html", context)
#     if request.method == "GET":
#         return response
#     elif request.method == "POST":
#         url = request.POST.get("URL")

#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         github = request.POST.get("GITHUB")

#         # password = request.POST.get("Password")
#         # retype_password = request.POST.get("Retype_password")
#         host = request.POST.get("HOST")
#         # first method to handle user name exist, can be optimize later
#         if validActor(username, password):
#             messages.error(request, 'User name exists!')
#             return response
#         else:
#             if retype_password != password:
#                 messages.error(request, 'Password does not match!')
#                 return response
#             createAuthor(host, username, url, github)
#             createActor(username, password)
#             cur_user_name = username
#             response = redirect("/chat/home/")
#             return response
#         # second method to handle user name exist, can be optimize later
#         if createAuthor("this", username, url, github):
#           return redirect("/chat/profile/")
#         else:
#           messages.error(request, 'User name exists!')
#           return render(request, "chat/signup.html", context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("test, beofore if")
        print("request : ", request.POST)
        print("form. : ", form)

        # if form.is_valid():
        print("gugua, in  if")
        # form.save()
        # username = form.cleaned_data.get('username')
        # raw_password = form.cleaned_data.get('password1')
        username = request.POST['username']
        raw_password = request.POST['password1']

        user = authenticate(username=username, password=raw_password)
        print("authenticate, in  if")
        login(request, user)
        print("test, in  if")
        return redirect('registration/profile.html')


    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})



"""
Generate response at home page  
"""
@login_required
def home(request):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    cur_author = request.user
    # a list of post
    mytimeline = cur_author.profile.TIMELINE.all() #getTimeline(cur_user_name)

    author_num_follwers = len(cur_author.profile.FOLLOWERS.all())

    dynamic_contain = {
        'myName' : cur_author.profile.DISPLAY_NAME,
        'timeline': mytimeline,
        'author_num_follwers': author_num_follwers

    }


    response = render(request, "chat/home.html", dynamic_contain)

    # query to database

    if request.method == "GET":

        return response
    elif request.method == "POST":

        # change later
        return response


"""
Generate response at friend_profile page , Now is deafault friend Zoe, need to be handled later 
"""
@login_required
def friend_profile(request):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    timeline = {}

    response = render(request, "chat/friendProfile.html", timeline)
    return response



"""
Generate response at feed page ,
"""
@login_required
def make_post(request):
    """
    so far, only support text-only post and post with img and caption
    Prob: 1. createPost return error!
    """
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    cur_author = request.user.profile
    mytimeline = cur_author.TIMELINE.all() #getTimeline(cur_user_name)
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
            return response
        else:
            print("sever feels sad ", description)

        response = render(request, "chat/feed.html", dynamic_contain)
        return response



"""
Generate response at my profile page , 
"""
@login_required
def profile(request):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    author = request.user.profile
    form = ProfileForm()
    form.fields['User_name'].initial = author.DISPLAY_NAME
    form.fields['Host'].initial = author.HOST
    form.fields['Url'].initial = author.URL
    form.fields['GitHub'].initial = author.GITHUB
    context = {}
    context['form']= form
    context['myName']= author.DISPLAY_NAME

    # query to database
    if request.method == "GET":
        response = render(request, "chat/myProfile.html", context)
        return response
    elif request.method == "POST":
        url = request.POST.get("Url")
        username = request.POST.get("User_name")
        github = request.POST.get("GitHub")
        # host = request.POST.get("Host")
        updateProfile(username, url, github)
        response = render(request, "chat/myProfile.html", context)
        return response


"""
REST Author, Generate response at my profile page , 
"""
@login_required
def profile_obj(request):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    author = request.user.profile

    obj = {
    "type":"author",
    # ID of the Author
    "id": author.URL,
    # the home host of the author
    "host": author.HOST,
    # the display name of the author
    "displayName": author.DISPLAY_NAME,
    # url to the authors profile
    "url": author.URL,
    # HATEOS url for Github API
    "github": author.GITHUB
    }


    # query to database
    if request.method == "GET":
        return  json.dumps(obj)
    elif request.method == "POST":

        post_obj = json.loads(request.body)
        url = post_obj["url"]
        displayName = post_obj["displayName"]
        github = post_obj["github"]
        # we do not allowed leave our server
        # host = post_obj["host"]
        updateProfile(displayName, url, github)
        return post_obj



# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })

"""
Generate response ,when delete user at home page , 
For user frinedly feature 
"""
@login_required
@require_http_methods(["DELETE", "POST"])
def delete(request, ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]
    cur_author = request.user.profile #getAuthor(cur_user_name)
    deletePost(ID)
    response = redirect("/chat/home/")
    return response


"""
Generate response ,when delete user at feed page , 
"""
# only allowed DELETE or POST to delete feed's post
@login_required
@require_http_methods(["DELETE", "POST"])
def delete_in_feed(request, ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]

    deletePost(ID)
    response = redirect("/chat/feed/")
   
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
