from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post
from .form import InputForm


# Create your views here.
def index(request):
    latest_list = Author.objects.order_by('host')[:5]
    context = {'latest_list': latest_list}
    # return render(request, 'chat/index.html', context)
    return render(request, '../templates/timeline2.html', context)


# Create your views here.
def home_view(request):
    context ={}
    context['form']= InputForm()
    return render(request, "chat/signup.html", context)
