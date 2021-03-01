from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm


# Create your views here.
def home(request):
	#context = {}
    latest_list = Post.objects.all()
    context = {'latest_list': latest_list}
    return render(request, 'chat/home.html', context)

# Create your views here.
def home_view(request):
    context ={}
    context['form']= InputForm()
    return render(request, "chat/signup.html", context)

def login(request):
	context = {}
	return render(request, "chat/login.html", context)

def signup(request):
	context = {}
	return render(request, "chat/signup.html", context)

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