from django.shortcuts import render
from django.http import HttpResponse
from .models import Author
from .models import Post
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

# Create your views here.
def index(request):
    latest_list = Author.objects.all()
    context = {'latest_list': latest_list}
    Author.objects.create(HOST='cat', DISPLAY_NAME='cat', URL='cat', GITHUB='cat')
    return render(request, 'chat/index.html', context)

# ...
def usr_post(request, ID):
    post = get_object_or_404(Post, pk=ID)
    try:
        post_content = Post.get(pk=request.POST['post'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'post': post,
            'error_message': "You didn't select a choice.",
        })
    else:
        post_content.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(post.id,))) # 'polls:results'