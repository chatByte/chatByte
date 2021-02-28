from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post

# Create your views here.
def index(request):
    latest_list = Author.objects.all()
    context = {'latest_list': latest_list}
    # Author.objects.create(HOST='cat', DISPLAY_NAME='cat', URL='cat', GITHUB='cat')
    return render(request, 'chat/index.html', context)