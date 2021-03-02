from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm
from .api import deletePost, addFriend, getAuthor, getTimeline
from django.core import serializers


"""
views.py receive request and create repose to client
"""
cur_author = None

# deisign

# cur_author obj created
# Create your views here.
def home(request):

    #context = {}
    latest_list = Post.objects.all()
    context = {'latest_list': latest_list}
    # print("---------------------", getAuthor("kuro"))
    return render(request, 'chat/home.html', context)

    # from jeremy
    # change a field in the post
    post = Post.objects.filter(SOURCE='changed')[0]
    # assuming obj is a model instance
    serialized_obj = serializers.serialize('json', [ post, ])
    print(serialized_obj)
    print(getAuthor('nothing'))
    addFriend("cat", "123")
    # deletePost(post.ID)
    return render(request, 'chat/index.html', context)


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

    # hard coding ??
    cur_author = getAuthor('Ritsu Onodera')


    dynamic_contain = {

        'fullName': cur_author.DISPLAY_NAME
        
    }

    # query to database
    # timeline = 


    # getTimeline()
    return render(request, "chat/timeline1.html", dynamic_contain)


def others_timeline(request):
    timeline = {}
    # query to database
    # timeline = 
    return render(request, "chat/timeline2.html", timeline)

def make_post(request):
    # post = {}

    # hard coding ??
    cur_author = getAuthor('Ritsu Onodera')
    # ??

    # testcase
    dynamic_contain = {  
        'fullName':'Ritsu Onodera',
        
        'test_name': cur_author.DISPLAY_NAME
    }  
    # Get the current pages' author



    # get post
    return render(request, "chat/feed.html", dynamic_contain)

def profile(request):
    author = {}
    # query to database
    return render(request, "chat/profile.html", author)