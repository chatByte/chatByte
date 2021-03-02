from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm, CreateAuthorForm
from .api import *
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
	#context = {}
    context = {}
    context['form']= InputForm()
    if request.method == "GET":
    	return render(request, "chat/home.html", context)
    elif request.method == "POST":
    	form = AuthenticationForm(request, request.POST)
    	if form.is_valid():
    		return redirect("/chat/profile")
    	else:
    		return render(request, 'chat/home.html', {'form': form})
   

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
		print("woohoo---------", request.POST.get("Url"))
		url = request.POST.get("Url")
		username = request.POST.get("User_name")
		github = request.POST.get("Github")
		password = request.POST.get("Password")
		createAuthor("this", username, url, github, password)
		return redirect("/chat/profile/")

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
