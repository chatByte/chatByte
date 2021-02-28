from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post

# Create your views here.
def index(request):
    latest_list = Post.objects.all()
    context = {'latest_list': latest_list}
    # Author.objects.create(HOST='cat', DISPLAY_NAME='cat', URL='cat', GITHUB='cat')
    # author = Author.objects.get(HOST="cat")
    # Post.objects.create(TITLE='', SOURCE='testing', ORIGIN='', DESCIPTION='', CONTENT_TYPE='', CONTENT=''\
    #     , AUTHOR=author, CATEGORIES='', COMMENTS_NO=0, PAGE_SIZE=0, COMMENTS_FIRST_PAGE='', VISIBILITY='public')
    return render(request, 'chat/index.html', context)