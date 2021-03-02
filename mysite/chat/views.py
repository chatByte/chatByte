from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm
from .api import deletePost, addFriend, getAuthor
from django.core import serializers

# Create your views here.
def home(request):
    #context = {}
    latest_list = Post.objects.all()
    context = {'latest_list': latest_list}
    print("---------------------", getAuthor("kuro"))
    return render(request, 'chat/home.html', context)
    # Create an author
    # Author.objects.create(HOST='cat', DISPLAY_NAME='cat', URL='cat', GITHUB='cat')

    # Create a post
    # author = Author.objects.get(HOST="cat")
    # Post.objects.create(TITLE='', SOURCE='testing', ORIGIN='', DESCIPTION='', CONTENT_TYPE='', CONTENT=''\
    #     , AUTHOR=author, CATEGORIES='', COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY='public')

    # change a field in the post
    # post = Post.objects.filter(SOURCE='changed')[0]
    # # assuming obj is a model instance
    # serialized_obj = serializers.serialize('json', [ post, ])
    # print(serialized_obj)
    # print(getAuthor('cat'))
    # addFriend("cat", "123")
    # # deletePost(post.ID)
    # return render(request, 'chat/index.html', context)

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