from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from .signals import host as host_server
from rest_framework.parsers import JSONParser

from .form import *
from .backend import *
from .signals import host
import base64
import os
import json
from .remoteProxy import *

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView



"""
views.py receive request and create repose to client,
Create your views here.
"""
# =============================================================================

from pagedown.forms import ImageUploadForm


IMAGE_UPLOAD_PATH = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_PATH', 'pagedown-uploads')
IMAGE_UPLOAD_UNIQUE = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_UNIQUE', False)
IMAGE_UPLOAD_ENABLED = getattr(
    settings, 'PAGEDOWN_IMAGE_UPLOAD_ENABLED', False)


@login_required
def image_upload_view(request):
    if not request.method == 'POST':
        raise PermissionDenied()

    if not IMAGE_UPLOAD_ENABLED:
        raise ImproperlyConfigured('Image upload is disabled')

    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES['image']
        path_args = [IMAGE_UPLOAD_PATH, image.name]
        if IMAGE_UPLOAD_UNIQUE:
            path_args.insert(1, str(uuid.uuid4()))
        path = os.path.join(*path_args)
        path = default_storage.save(path, image)
        url = default_storage.url(path)
        return JsonResponse({'success': True, 'url': url})

    return JsonResponse({'success': False, 'error': form.errors})
# =============================================================================
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
    mytimeline = cur_author.profile.timeline

    # Get stream from: node origins, since we have plenty remote server
    for node in Node.objects.all():
        print("Get stream from: ", node.origin)
        print("Username: ", node.username, " password: ", node.password)
        res = streamRequest(node.origin, request.user.id)
        try:
            data = res.json()
            # print(data['posts'])
            for post in data['posts']:
                # print("Post id: ", post['id'])
                post_id = post['id']
                try:
                    post_obj = Post.objects.get(id=post_id)
                except Post.DoesNotExist:
                    author_dict = post['author']
                    # print("Author dict: ", author_dict)
                    try:
                        author = Profile.objects.get(id=author_dict['id'])
                    except Profile.DoesNotExist:
                        author_serializer = ProfileSerializer(data=author_dict)
                        if author_serializer.is_valid(raise_exception=True):
                            author = author_serializer.save()
                    comments_dict = post['comments']
                    comments_list = list()
                    for comment in comments_dict:
                        # print("Comment: ", comment)
                        try:
                            comment_obj = Comment.objects.get(id=comment['id'])
                            comments_list.append(comment_obj)
                        except Comment.DoesNotExist:
                            comm_author_dict = comment['author']
                            print("Comment author: ", comm_author_dict)
                            try:
                                comm_author = Profile.objects.get(id=comm_author_dict['id'])
                            except Profile.DoesNotExist:
                                author_serializer = ProfileSerializer(data=comm_author_dict)
                                if author_serializer.is_valid(raise_exception=True):
                                    comm_author = author_serializer.save()
                            comment_serializer = CommentSerializer(data=comment)
                            print(comment_serializer)
                            if comment_serializer.is_valid(raise_exception=True):
                                comment_obj = comment_serializer.save(author=comm_author)
                                print("Created comment obj: ", comment_obj)
                                comments_list.append(comment_obj)

                    serializer = PostSerializer(data=post)
                    # print("here")
                    # print(serializer)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save(author=author) # comments=comments_list
                        post_obj = Post.objects.get(id=post_id)
                # add stream post into public channel
                mytimeline.add(post_obj)
                # print("Post object", post_obj)
        except BaseException as e:
            print(e)



    # a group of author, that i am currently following, django.db.models.query.QuerySet
    followings = cur_author.profile.followings.all()

    # merging quesryset
    public_channel_posts = mytimeline.all()

    for following_profile in followings:

        public_posts = following_profile.timeline.filter(visibility='public')
        public_channel_posts = public_channel_posts | public_posts


    author_num_follwers = len(cur_author.profile.followers.items.all())
    friend_request_num = len(cur_author.profile.friend_requests.all())
    # order by date
    public_channel_posts = public_channel_posts.order_by('-published')

    # create a paginator
    paginator_public_channel_posts = Paginator(public_channel_posts, 8) # Show 8 contacts per page.

    # if  page_number == None, we will get first page(can be empty)
    page_number = request.GET.get('page')


    page_obj = paginator_public_channel_posts.get_page(page_number)


    dynamic_contain = {
        'myName' : cur_author.profile.displayName,
        'public_channel_posts': public_channel_posts,
        'page_obj': page_obj,
        'author_num_follwers': author_num_follwers,
        'friend_request_num': friend_request_num
    }


    if request.method == "GET":
        response = render(request, "chat/stream.html", dynamic_contain)
        return response

    elif request.method == "POST":

        request_post = request.POST
        # Front end need to tell me the type
        print("_________________________________________________________")
        print(type(request_post))


        # source = request.user.profile.id # Who share it to me
        # origin = host_server # who origin create
        # title = request_post.get("title", "")
        # description = request_post.get("description", "")
        # content_type = request_post.get("contentType", "")
        # visibility = request_post.get("visibility", "")

        testing_response = render(request, "chat/stream.html", dynamic_contain)
        return testing_response




"""
Generate response at friend_profile page , Now is deafault friend Zoe, need to be handled later
"""
@login_required
def foreign_public_channel(request, AUTHOR_ID, SERVER, FOREIGN_ID):
    server = User.objects.get(username=SERVER)
    host = server.last_name
    foreign_author = getUser(FOREIGN_ID)
    author_id = host + "author/" + AUTHOR_ID
    cur_author = Profile.objects.get(id=author_id)
    if foreign_author != None:
        foreign_user_name = foreign_author.username

        if getFriend(request.user.id, foreign_author.id):
            isFriend = True;
        else:
            isFriend = False;

        if getFollowing(request.user.id, foreign_author.id):
            isFollowing = True;
        else:
            isFollowing = False;

        # a list of post
        #foreign_timeline = foreign_author.profile.timeline.all() #getTimeline(cur_user_name)
        foreign_timeline = postsRequest("GET", host, FOREIGN_ID).json()['posts']
        foreign_timeline = PostSerializer(foreign_timeline, many=True).data

        author_num_follwers = len(foreign_author.profile.followers.items.all())
        friend_request_num = len(foreign_author.profile.friend_requests.all())

        dynamic_contain = {
            'foreignName' : foreign_author.profile.displayName,
            'timeline': foreign_timeline,
            'author_num_follwers': author_num_follwers,
            'isFriend': isFriend,
            'isFollowing': isFollowing,
            'foreignId':foreign_author.id,
            'friend_request_num': friend_request_num,
            'cur_author': cur_author,
        }
        response = render(request, "chat/foreign_public_channel.html", dynamic_contain)
        return response
    return HttpResponse(404)



"""
Generate response at feed page ,
"""
@login_required
@require_http_methods(["GET", "POST"])
def posts(request, AUTHOR_ID):
    """
    so far, only support text-only post and post with img and caption
    """
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    cur_author = request.user.profile
    alltimeline = cur_author.timeline.all()
    #getTimeline(cur_user_name), by SQL query
    mytimeline = alltimeline.filter(author=cur_author).order_by('-published')

    
    # create a paginator
    paginator_mytimeline = Paginator(mytimeline, 8) # Show 8 contacts per page.

    # if  page_number == None, we will get first page(can be empty)
    page_number = request.GET.get('page')


    page_obj = paginator_mytimeline.get_page(page_number)


    author_num_follwers = len(cur_author.followers.items.all())
    friend_request_num = len(cur_author.friend_requests.all())



    dynamic_contain = {
        'fullName':'Ritsu Onodera',
        'author_num_follwers': author_num_follwers,
        'test_name': cur_user_name,
        'myName' : cur_author.displayName,
        'page_obj' : page_obj,
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


# Method that generate a friend request
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



@require_http_methods(["GET"])
@login_required
def add_follow(request, AUTHOR_ID, FOREIGN_AUTHOR_ID):
    try:
        addFollow(request.user.id, FOREIGN_AUTHOR_ID)
        return HttpResponse(status=200)
    except BaseException as e:
        return HttpResponse(status=401)

@require_http_methods(["GET"])
@login_required
def get_user(request,SERVER,AUTHOR_ID):
    # get
    print("---------------------------Getting user ---------------")
    try:
        server = User.objects.get(username=SERVER)
        foreign_server = server.last_name
        user_id = foreign_server + "author/"+ AUTHOR_ID
        profile = Profile.objects.get(id=user_id)
        type = profile.type
        id = profile.id
        host = profile.host
        displayName = profile.displayName
        github = profile.github
        url = profile.url
        return JsonResponse({'type':type, 'id':id, 'host':host, 'displayName':displayName, 'github':github, "url":url}, status=200)
    except BaseException as e:
        print(e)
        return HttpResponse(status=400)

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



'''
search a specifc user ID, redirect to http://127.0.0.1:8000/author/1/my_stream/2/#
'''
@require_http_methods(["POST"])
@login_required
def search(request, AUTHOR_ID):
    server_origin = request.META["HTTP_X_SERVER"]
    user = User.objects.get(last_name=server_origin)
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    data = JSONParser().parse(request)

    try:
        target_id = data["url"]
        author_origin = "https://" + target_id.split("/")[2] + "/"
    except:
        return JsonResponse({}, status=409)
    try:
        target = Profile.objects.get(id=target_id)
        serializer = ProfileSerializer(target)

        numberID_target = target_id.split("/")[-1]
        server_name = user.username


        # return response
        redirect_url = "../my_stream/" + server_name +"/" + numberID_target + "/"


        json_dict = {"url": redirect_url}

        return JsonResponse(json_dict, status=200)
    except Profile.DoesNotExist:
        response = profileRequest("GET", author_origin, target_id.split("/")[-1])
        #print(author_origin)

        if response.status_code == 200:
            foreign_author = response.json()
            # foreign_author = {'type': 'author',
            #                 'id': 'http://127.0.0.1:5000/author/10',
            #                 'host': 'http://127.0.0.1:5000/author/10',
            #                 'displayName': 'Jonathan',
            #                 'url': 'http://127.0.0.1:5000/author/10',
            #                 'github': 'http://127.0.0.1:5000/author/10'}
            serializer = ProfileSerializer(data=foreign_author)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"url": "../mystream/2/"}, status=200)
        else:
            return JsonResponse(response.json(), status=response.status_code)



'''
create a following, add foreigner to be my followings
'''
@login_required
@require_http_methods(["POST", "PUT"])
def following(request, AUTHOR_ID, SERVER, FOREIGN_ID):
    server = User.objects.get(username=SERVER)
    foreign_server = server.last_name
    AUTHOR_ID = host_server + "author/"+ AUTHOR_ID
    FOREIGN_ID = foreign_server + "author/"+ FOREIGN_ID
    foreigner = Profile.objects.get(id=FOREIGN_ID)
    profile = Profile.objects.get(id=AUTHOR_ID)
    profile.followings.add(foreigner)
    profile.save()
    return JsonResponse({}, status=204)


'''
Below is the dead code, or previous version, keep it , incase need that in the future


TOP=================================>


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

BOT<==================================================================

'''
