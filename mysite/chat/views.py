from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm, CreateAuthorForm
from .api import *
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
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
		# 	return redirect("/chat/profile/")
		# else:
		# 	messages.error(request, 'User name exists!')
		# 	return render(request, "chat/signup.html", context)

def my_timeline(request):
    timeline = {}
    # query to database
    # timeline = 
    return render(request, "chat/timeline1.html", timeline)

def others_timeline(request):
    timeline = {}
    # query to database
    # timeline = 
    return render(request, "chat/timeline2.html", timeline)

def make_post(request):
    post = {}
    # get post
    return render(request, "chat/feed.html", post)

def profile(request):
    author = {}
    # query to database
    return render(request, "chat/profile.html", author)