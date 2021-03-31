from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .signals import host as host_server
from rest_framework.parsers import JSONParser

from .form import *
from .backend import *
from .signals import host
import base64
import os
import json
from .remoteProxy import *



"""
views.py receive request and create repose to client,
Create your views here.
"""


@login_required
def start_homepage(request):
    if request.user.is_authenticated:
        return redirect("/author/" + str(request.user.id) + "/profile/")
    else: return redirect("/accounts/login/")




def signup(request):
    form = UserCreationForm(request.POST)
    print("--------------", request.POST)
    print("--------------", form)
    form.non_field_errors()
    field_errors = [ (field.label, field.errors) for field in form]
    print(field_errors)

    if form.is_valid():
        print("is valid")
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        print("authenticating...")
        user = authenticate(username=username, password=password)
        print("logging in...")
        login(request, user)

        return redirect('/author/' + str(user.id) + "/profile/")
    return render(request, 'registration/signup.html', {'form': form})



"""
Generate response at home page  => eveyones' post here
path(r"author/<str:AUTHOR_ID>/public_channel/",
"""
# get feed and
# post: comment/like => send post request to host server(edit post function),
@require_http_methods(["GET", "POST"])
@login_required
def my_stream(request, AUTHOR_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username

    cur_author = request.user
    # a list of post, django.db.models.query.QuerySet
    mytimeline = cur_author.profile.timeline.all()
    # a group of author, that i am currently following, django.db.models.query.QuerySet
    followings = cur_author.profile.followings.all()

    # merging quesryset
    public_channel_posts = mytimeline

    for following_profile in followings:


        public_posts = following_profile.timeline.filter(visibility='public')
        public_channel_posts = public_channel_posts | public_posts


    author_num_follwers = len(cur_author.profile.followers.items.all())
    friend_request_num = len(cur_author.profile.friend_requests.all())
    # order by date
    public_channel_posts = public_channel_posts.order_by('published')

    dynamic_contain = {
        'myName' : cur_author.profile.displayName,
        # 'timeline': mytimeline,

        'public_channel_posts': public_channel_posts,
        'author_num_follwers': author_num_follwers,
        'friend_request_num': friend_request_num
    }


    response = render(request, "chat/stream.html", dynamic_contain)
    return response


"""
Generate response at friend_profile page , Now is deafault friend Zoe, need to be handled later
"""
@login_required
def friend_public_channel(request, AUTHOR_ID, FOREIGN_ID):
    cur_author = getUser(FOREIGN_ID)
    cur_user_name = cur_author.username

    if getFriend(request.user.id, cur_author.id):
        isFriend = True;
    else:
        isFriend = False;
    # a list of post
    mytimeline = cur_author.profile.timeline.all() #getTimeline(cur_user_name)

    author_num_follwers = len(cur_author.profile.followers.items.all())
    friend_request_num = len(cur_author.profile.friend_requests.all())

    dynamic_contain = {
        'myName' : cur_author.profile.displayName,
        'timeline': mytimeline,
        'author_num_follwers': author_num_follwers,
        'isFriend': isFriend,
        'myId':cur_author.id,
        'friend_request_num': friend_request_num,

    }
    response = render(request, "chat/friendProfile.html", dynamic_contain)
    return response



"""
Generate response at feed page ,
"""
@login_required
@require_http_methods(["GET", "POST"])
def posts(request, AUTHOR_ID):
    """
    so far, only support text-only post and post with img and caption
    Prob: 1. createPost return error!
    """
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    cur_author = request.user.profile
    alltimeline = cur_author.timeline.all()
    #getTimeline(cur_user_name), by SQL query
    mytimeline = alltimeline.filter(author=cur_author).order_by('published')

    author_num_follwers = len(cur_author.followers.items.all())
    friend_request_num = len(cur_author.friend_requests.all())

    dynamic_contain = {
        'fullName':'Ritsu Onodera',
        'author_num_follwers': author_num_follwers,
        'test_name': cur_user_name,
        'myName' : cur_author.displayName,
        'timeline': mytimeline,
        'friend_request_num': friend_request_num,

    }

    # Get the current pages' author

    if request.method == "GET":
        response = render(request, "chat/posts.html", dynamic_contain)
        return response

    elif request.method == "POST":

        request_post = request.POST

        source = request.user.profile.id # Who share it to me
        origin = host_server # who origin create
        title = request_post.get("title", "")
        description = request_post.get("description", "")
        content_type = request_post.get("contentType", "")
        visibility = request_post.get("visibility", "")

        f = request.FILES.get("file", "")
        categories = ["text/plain"] # web, tutorial, can be delete  # ?? dropdown


        if len(f) > 0:
            categories = "image/" + os.path.splitext(f.name)[-1][1:]
            with f.open("rb") as image_file:
                content = base64.b64encode(image_file.read())
        else:
            content = description

        createFlag = createPost(title, source, origin, description, content_type, content, request.user.profile, categories, visibility)
        if createFlag:
            print("haha, successful create post, info: ", description)

            # response = redirect("/author/"+ str(AUTHOR_ID) + "/public_channel/")
            response = HttpResponse(status=200)
            return response
        else:
            print("server feels sad ", description)

        response = render(request, "chat/posts.html", dynamic_contain)
        return response



"""
Generate response at my profile page ,
"""
@login_required
@require_http_methods(["GET", "POST"])
def profile(request, AUTHOR_ID):
    user = None
    if request.user.is_authenticated:
        user = request.user
    profile = request.user.profile
    form = ProfileForm()
    form.fields['email'].initial = user.email
    form.fields['URL'].initial = profile.url
    form.fields['GITHUB'].initial = profile.github
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
    context = {}
    context['form']= form

    friend_request_num = len(profile.friend_requests.all())

    context['friend_request_num']=friend_request_num


    # query to database
    if request.method == "GET":
        # check if this is my profile or other's profile
        response = render(request, "chat/profile.html", context)
        return response
    elif request.method == "POST":
        post_obj = request.POST
        url = post_obj["URL"]
        email = post_obj["email"]
        github = post_obj["GITHUB"]
        first_name = post_obj["first_name"]
        last_name = post_obj["last_name"]
        updateProfile(user.id, first_name, last_name, email, url, github)
        response = redirect("/author/"+ str(request.user.id) + "/profile/")
        return response


"""
Generate response ,when delete user at home page ,
For user frinedly feature
"""
@login_required
@require_http_methods(["DELETE", "POST"])
def delete(request, ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]
    cur_author = request.user.profile #getAuthor(cur_user_name)
    deletePost(ID)

    # TODO: may not redirect
    response = redirect("/author/"+ str(request.user.id) + "/public_channel/")
    return response


def edit(request, ID):
    print(request.POST)
    new_description = request.POST.get("editText")
    print(new_description)
    editPostDescription(ID, new_description)
    # TODO: may not redirect
    response = redirect("/chat/feed/")

    return response

# delete later
# get feed and
# post: comment/like => send post request to host server(edit post function),
@require_http_methods(["GET", "POST"])
def edit_in_feed(request, ID):
    print(request.POST)
    new_description = request.POST.get("editText")
    print(new_description)
    print(editPostDescription(ID, new_description))
    response = redirect("/chat/feed/")

    return response



@login_required
@require_http_methods(["GET"])
@login_required
def my_friends(request,AUTHOR_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    print(cur_user_name)
    friend_list = getFriends(request.user.id)

    print(friend_list)
    cur_author = request.user.profile
    author_num_follwers = len(cur_author.followers.items.all())
    friend_request_num = len(cur_author.friend_requests.all())
    dynamic_contain = {
        'myName' : cur_author.displayName,
        'friend_list': friend_list,
        'author_num_follwers': author_num_follwers,
        'friend_request_num': friend_request_num
    }

    return render(request, "chat/myFriends.html", dynamic_contain)
    # return render(request, "chat/myFriends.html")

# @require_http_methods(["DELETE"])
# TODO: accept only DELETE? How to send delete request by HTML?
# Now using GET, prone to CSRF attack?
@login_required
def delete_friend(request, AUTHOR_ID, FRIEND_ID):
    try:
        cur_user_name = None
        if request.user.is_authenticated:
            cur_user_name = request.user.username
        deleteFriend(AUTHOR_ID, FRIEND_ID)
        return HttpResponse(status=200)

    except BaseException as e:
        print(e)
        return HttpResponse(status=401)
    return HttpResponse(status=304)

# @require_http_methods(["GET"])
@login_required
def add_friend(request, AUTHOR_ID, FRIEND_ID):
    print(AUTHOR_ID, FRIEND_ID)
    try:
        cur_user_name = None
        if request.user.is_authenticated:
            cur_user_name = request.user.username
        addFriendRequest(FRIEND_ID, AUTHOR_ID)
        return HttpResponse(status=200)
    except BaseException as e:
        print(e)
        return HttpResponse(status=401)
    return HttpResponse(status=304)


# AJAX request comes every 5 seconds
@require_http_methods(["GET"])
@login_required
def if_friend_request(request):
    try:
        cur_user_name = None
        if request.user.is_authenticated:
            cur_user_name = request.user.username

        all_friend_request = getALLFriendRequests(request.user.id)
        if len(all_friend_request)>0:
            newest = all_friend_request.reverse()[0]
            data = {}
            data['friend'] = newest.actor.displayName
            data['id'] = newest.id
            # return the newest friend request's name
            return JsonResponse(data)
        else:
            return HttpResponse(status=304)

    except BaseException as e:
        print(e)
        return HttpResponse(status=304)


@require_http_methods(["GET"])
@login_required
def accept_friend_request(request, AUTHOR_ID, FRIEND_REQUEST_ID):
    try:
        addFriendViaRequest(request.user.id, FRIEND_REQUEST_ID)
        deleteFriendRequest(request.user.id, FRIEND_REQUEST_ID)
        return HttpResponse(status=200)
    except BaseException as e:
        return HttpResponse(status=401)


@require_http_methods(["GET"])
@login_required
def reject_friend_request(request, AUTHOR_ID, FRIEND_REQUEST_ID):
    try:
        deleteFriendRequest(request.user.id, FRIEND_REQUEST_ID)
        return HttpResponse(status=200)
    except BaseException as e:
        return HttpResponse(status=401)


@login_required
@require_http_methods(["POST"])
def update_post(request, AUTHOR_ID, POST_ID):
    print('edited arguemnt POST_ID', str(POST_ID))
    id = host_server + 'author/' + str(AUTHOR_ID) + '/posts/' + str(POST_ID)
    print("edited post id:", id)
    user = None
    username=""
    if request.user.is_authenticated:
        user = request.user
        username = request.user.profile.displayName

    request_post = request.POST
    source = username # Who share it to me
    origin = username # who origin create
    title = request_post.get("title", "")
    description = request_post.get("description", "")
    content_type = request_post.get("contentType", "")
    visibility = request_post.get("visibility", "")
    f = request.FILES.get("file", "")
    categories = "text/plain" # web, tutorial, can be delete  # ?? dropdown
    if len(f) > 0:
        categories = "image/" + os.path.splitext(f.name)[-1][1:]
        with f.open("rb") as image_file:
            content = base64.b64encode(image_file.read())
    else:
        content = description

    updateFlag = updatePost(id, title, source, origin, description, content_type, content, categories, visibility)
    if updateFlag:
        print("Successful edited post, info: ", description)
        response = HttpResponse(status=200)
        return response
    else:
        print("failed to edit the post!!", description)
    
    response = redirect("/author/" + str(user.id) + "/my_posts/")
    return response
@require_http_methods(["POST"])
@login_required
def search(request, AUTHOR_ID):
    server_origin = request.META["HTTP_X_SERVER"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    print("...........................???.....")

    data = JSONParser().parse(request)

    try:
        target_id = data["url"]
        print(target_id)
    except:
        return JsonResponse({}, status=409)
    try:
        target = Profile.objects.get(id=target_id)
        serializer = ProfileSerializer(target)
        
        numberID_target = target_id.split("/")[-1]

        # 127.0.0.1:8000/author/1/my_stream/2
        # ID
        #http://127.0.0.1:8000/author/2
        response = redirect("../my_stream/" + numberID_target + "/")

        # return response
        redirect_url = "../my_stream/" + numberID_target + "/"


        json_dict = {"url": redirect_url}  

        return JsonResponse(json_dict, status=201)
    except Profile.DoesNotExist:
        return profileRequest("GET", server_origin, target_id)


@require_http_methods(["POST"])
@login_required
def search_user(request, AUTHOR_ID, FOREGIN_ID):
    server_origin = request.META["HTTP_X_SERVER"]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    # data = JSONParser().parse(request)
    # try:
    #     target_id = data["url"]
    # except:
    #     return JsonResponse({}, status=409)
    try:
        target = Profile.objects.get(id=FOREGIN_ID)
        serializer = ProfileSerializer(target)
        return JsonResponse(serializer.data, status=201)
    except Profile.DoesNotExist:
        return profileRequest("GET", server_origin, FOREGIN_ID)
