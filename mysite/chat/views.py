from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
# Create your views here.
def index(request):
    latest_list = Author.objects.order_by('host')[:5]
    context = {'latest_list': latest_list}
    return render(request, 'chat/index.html', context)