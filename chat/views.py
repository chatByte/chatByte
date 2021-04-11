from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
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

import requests



"""
views.py receive request and create repose to client,
Create your views here.
"""
# =============================================================================

# from pagedown.forms import ImageUploadForm


# IMAGE_UPLOAD_PATH = getattr(
#     settings, 'PAGEDOWN_IMAGE_UPLOAD_PATH', 'pagedown-uploads')
# IMAGE_UPLOAD_UNIQUE = getattr(
#     settings, 'PAGEDOWN_IMAGE_UPLOAD_UNIQUE', False)
# IMAGE_UPLOAD_ENABLED = getattr(
#     settings, 'PAGEDOWN_IMAGE_UPLOAD_ENABLED', False)


# @login_required
# def image_upload_view(request):
#     if not request.method == 'POST':
#         raise PermissionDenied()

#     if not IMAGE_UPLOAD_ENABLED:
#         raise ImproperlyConfigured('Image upload is disabled')

#     form = ImageUploadForm(request.POST, request.FILES)
#     if form.is_valid():
#         image = request.FILES['image']
#         path_args = [IMAGE_UPLOAD_PATH, image.name]
#         if IMAGE_UPLOAD_UNIQUE:
#             path_args.insert(1, str(uuid.uuid4()))
#         path = os.path.join(*path_args)
#         path = default_storage.save(path, image)
#         url = default_storage.url(path)
#         return JsonResponse({'success': True, 'url': url})

#     return JsonResponse({'success': False, 'error': form.errors})
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
        user = form.save(commit=False)
        # sets the field to False
        user.is_active=False
        user.save()
        username = form.cleaned_data.get('username')
        messages.success(request, f'Your account has been created! You are now able to log in')
        return redirect('login')

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
    back_json = get_github_activity(request, AUTHOR_ID)
    # print("github", back_json)

    if request.method == "GET":

        # a list of post, django.db.models.query.QuerySet
        # mytimeline = cur_author.profile.timeline
        mytimeline = cur_author.profile.timeline.filter(unlisted=False)
        all_public_posts = Post.objects.filter(visibility='public').filter(unlisted=False).all()

        back_json = get_github_activity(request, AUTHOR_ID)

        # Get stream from: node origins, since we have plenty remote server
        remote_posts = []
        for node in Node.objects.all():
            # print("Get stream from: ", node.origin)
            # print("Username: ", node.username, " password: ", node.password)

            if node.origin == host_server:
                continue

            res = streamRequest(node.origin, request.user.id)
            try:
                data = res.json()
                # remote_posts += data['posts']
                # print(data['posts'])
                for post in data['posts']:
                    remote_post_id = post['id']
                    remote_origin = remote_post_id.split('author/')[0]
                    remote_user_id = remote_post_id.split('author/')[1].split('/posts/')[0]
                    remote_post_id = remote_post_id.split('author/')[1].split('posts/')[1]
                    res = likesRequest("GET", remote_origin, remote_user_id, remote_post_id)
                    print("stream get post's likes: ", res.json())
                    print("Number of likes: ", len(res.json()))
                    post['num_likes'] =  len(res.json())
                    for comment in post['comments']:
                        print(comment['id'])
                        comment_id = comment['id'].split('comments/')[1]
                        com_res = commentLikesRequest("GET", remote_origin, remote_user_id, remote_post_id, comment_id)
                        comment['num_likes'] = len(com_res.json())
                        print(comment['num_likes'])
                    remote_posts.append(post)

                #     # print("Post id: ", post['id'])
                #     post_id = post['id']
                #     try:
                #         post_obj = Post.objects.get(id=post_id)
                #         serializer = PostSerializer(post_obj, data=post, partial=True)
                #         if serializer.is_valid(raise_exception=True):
                #             serializer.save()
                #     except Post.DoesNotExist:
                #         author_dict = post['author']
                #         # print("Author dict: ", author_dict)
                #         try:
                #             author = Profile.objects.get(id=author_dict['id'])
                #         except Profile.DoesNotExist:
                #             author_serializer = ProfileSerializer(data=author_dict)
                #             if author_serializer.is_valid(raise_exception=True):
                #                 author = author_serializer.save()

                #         serializer = PostSerializer(data=post)

                #         if serializer.is_valid(raise_exception=True):
                #             serializer.save(author=author) # comments=comments_list
                #             post_obj = Post.objects.get(id=post_id)
                #     # add stream post into public channel
                #     mytimeline.add(post_obj)
                #     # print("Post object", post_obj)

            except BaseException as e:
                print(e)



        # a group of author, that i am currently following, django.db.models.query.QuerySet
        followings = cur_author.profile.followings.all()

        # similar to followings, but a list of Friends
        myFriends = cur_author.profile.friends

        # merging quesryset
        public_channel_posts = mytimeline.all()

        for following_profile in followings:

            public_posts = following_profile.timeline.filter(visibility='public')
            public_channel_posts = public_channel_posts | public_posts

        jsonify_public_channel_posts = []
        for post in public_channel_posts:
            post_num_likes = len(post.likes.all())
            comment_like_list = []
            for comment in post.comments.all():
                comment_num_likes = len(comment.likes.all())
                comment_like_list.append(comment_num_likes)
            json_post = json.loads(json.dumps(PostSerializer(post).data))
            for i in range(len(json_post['comments'])):
                json_post['comments'][i]['num_likes'] = comment_like_list[i]
            json_post['num_likes'] = post_num_likes
            jsonify_public_channel_posts.append(json_post)
        # PostSerializer(public_channel_posts, many=True).data
        # print("PostSerializaer:\n", json.dumps(PostSerializer(public_channel_posts, many=True).data))
        # public_channel_posts = json.loads(json.dumps(PostSerializer(public_channel_posts, many=True).data)) + remote_posts # a list
        # print("public_channel_posts:\n", public_channel_posts)
        jsonify_public_channel_posts += remote_posts

        author_num_follwers = len(cur_author.profile.followers.items.all())
        friend_request_num = len(cur_author.inbox.friend_requests.all())
        # order by date
        # public_channel_posts = public_channel_posts.order_by('-published')

        jsonify_public_channel_posts = sorted(jsonify_public_channel_posts, key=lambda k: k.get('published', 0), reverse=True)
        for post in jsonify_public_channel_posts:
            print("post:\n", post)
            post['comments'] = sorted(post['comments'], key=lambda k: k.get('published', 0))


        # create a paginator
        paginator_public_channel_posts = Paginator(jsonify_public_channel_posts, 8) # Show 8 contacts per page.

        print("--------------------")
        print(paginator_public_channel_posts)

        # if  page_number == None, we will get first page(can be empty)
        page_number = request.GET.get('page')


        page_obj = paginator_public_channel_posts.get_page(page_number)

        liked_objs = cur_author.profile.liked.items.values_list('object', flat=True)
        # print("Liked objects: ", liked_objs)
        # print(list(public_channel_posts)[0].likes)

        dynamic_contain = {
            'myName' : cur_author.profile.displayName,
            'public_channel_posts': public_channel_posts,
            'page_obj': page_obj,
            'author_num_follwers': author_num_follwers,
            'friend_request_num': friend_request_num,
            'liked_objs': liked_objs,
            'friends': myFriends,
            'git_activity_obj': back_json,
            'remote_post': remote_posts
        }


        response = render(request, "chat/stream.html", dynamic_contain)

        return response

    elif request.method == "POST":

        request_post = JSONParser().parse(request)
        # Front end need to tell me the type
        contentType = request_post.get("type","")
        cur_author_id = cur_author.profile.id

        if contentType == "like":
            object_type = request_post.get("object_type","")
            object_id = request_post.get("object_id","")
            # Determine if the liked object is remote or local
            server_origin = object_id.split('author/')[0]
            if server_origin not in host_server:
                print("Sending like to remote server...")
                if object_type == "post":
                    like = Like.objects.create(author=request.user.profile, object=object_id, summary= request.user.profile.displayName + " likes a post")
                else:
                    like = Like.objects.create(author=request.user.profile, object=object_id, summary= request.user.profile.displayName + " likes a comment")
                # send the like object to remote server
                res = inboxRequest("POST", server_origin, AUTHOR_ID, {"type": "like", "data": {"type": object_type, "id": object_id}})
                if res.status_code < 400:
                    print("liked object successfully")
                    # store liked object in current author
                    request.user.profile.liked.items.add(like)
                    request.user.profile.liked.save()
                    
                else:
                    like.delete()
                return JsonResponse(res.json(), status=res.status_code)
            else:
                if object_type == "post":

                    likePost(object_id, cur_author_id)

                    response = JsonResponse({'redirect_url': "current"}, status=200)
                    # response = render(request, "chat/stream.html", dynamic_contain)
                elif object_type == "comment":

                    # object_id = request_post.get("object_id","")
                    likeComment(object_id, cur_author_id)
                    # response = render(request, "chat/stream.html", dynamic_contain)
                    # pass
                    response = JsonResponse({'redirect_url': "current"}, status=200)
                else:
                    response = JsonResponse({"Details", "Invalid like object type"}, status=400)

        elif contentType == "comment":

            post_id = request_post.get("post_id","")
            comment_contain = request_post.get("comment","")
            comment_content_type = request_post.get("content_type","")

            #if successful create a comment
            # if  createComment(cur_author.profile, post_id, comment_contain, comment_content_type) :
            #     response = JsonResponse({'redirect_url': "current"}, status=200)
            send_data = {
                'content': comment_contain,
                'contentType': comment_content_type
            }
            # response = request.post(post_id + "/comments", data=json.dumps(send_data), head)
            response = commentRequest("POST", post_id.split('author/')[0], post_id.split('author/')[1].split('/posts/')[0] \
                , post_id.split('author/')[1].split('/posts/')[1], send_data)

            print("response json:", response.json())
            return JsonResponse(response.json(), status=response.status_code)
            # else:
            #     response = JsonResponse({}, status=500)

        else:
            response = JsonResponse({}, status=400)

        return response




"""
Generate response at friend_profile page , Now is deafault friend Zoe, need to be handled later
"""
@login_required
def foreign_public_channel(request, AUTHOR_ID, SERVER, FOREIGN_ID):
    server = User.objects.get(username=SERVER)
    host = server.last_name
    # foreign_author = getUser(FOREIGN_ID)
    foreign_author = Profile.objects.get(id=host + "author/" + FOREIGN_ID)
    author_id = host_server + "author/" + AUTHOR_ID
    print(author_id)
    cur_author = Profile.objects.get(id=author_id)
    # if foreign_author != None:
    #     foreign_user_name = foreign_author.username

    #     if getFriend(request.user.id, foreign_author.id):
    #         isFriend = True;
    #     else:
    #         isFriend = False;

    #     if getFollowing(request.user.id, foreign_author.id):
    #         isFollowing = True;
    #     else:
    #         isFollowing = False;

        # a list of post
        #foreign_timeline = foreign_author.profile.timeline.all() #getTimeline(cur_user_name)
        # try:
        # res = postsRequest("GET", host, FOREIGN_ID)
        # if res.status_code < 400:
        #     foreign_timeline = PostSerializer(res.json()['posts'], many=True).data
        # else:
        #     foreign_timeline = []
        # except:
        #     foreign_timeline = []

        # author_num_follwers = len(foreign_author.profile.followers.items.all())
        # friend_request_num = len(request.user.inbox.friend_requests.all())

    dynamic_contain = {
        'foreignName' : foreign_author.displayName,
        'timeline': [],
        'author_num_follwers': 0,
        'isFriend': False,
        'isFollowing': False,
        'foreignId':foreign_author.id,
        'friend_request_num': 0,
        'cur_author': cur_author,
    }
    response = render(request, "chat/foreign_public_channel.html", dynamic_contain)
    return response
    # return HttpResponse(404)



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


    # Get the current pages' author
    if request.method == "GET":

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
        friend_request_num = len(request.user.inbox.friend_requests.all())



        dynamic_contain = {
            'fullName':'Ritsu Onodera',
            'author_num_follwers': author_num_follwers,
            'test_name': cur_user_name,
            'myName' : cur_author.displayName,
            'page_obj' : page_obj,
            'friend_request_num': friend_request_num
        }

        response = render(request, "chat/posts.html", dynamic_contain)
        return response

    elif request.method == "POST":

        request_post = request.POST
        source = "handled by backend" # Who share it to me
        origin = "handled by backend"  # who origin create
        title = request_post.get("title", "")
        description = request_post.get("description", "")
        content_type = request_post.get("contentType", "")
        visibility = request_post.get("visibility", "")
        unlisted = request_post.get("unlisted","")

        f = request.FILES.get("file", "")
        categories = request_post.get("categories","")


        if len(f) > 0:
            content_type = "image/" + os.path.splitext(f.name)[-1][1:]
            with f.open("rb") as image_file:
                content = base64.b64encode(image_file.read())
                content = str(content).decode('ascii')
                print(content)
        else:
            content = description

        createFlag = createPost(title, source, origin, description, content_type, content, request.user.profile, categories, visibility,unlisted)
        if createFlag:
            # print("haha, successful create post, info: ", description)

            # response = redirect("/author/"+ str(AUTHOR_ID) + "/public_channel/")
            response = HttpResponse(status=200)
            return response
        else:
            print("server feels sad ", description)
            # expect front end redirect
            response = JsonResponse({}, status=500)
        # response = render(request, "chat/posts.html", dynamic_contain)
        return response



'''
Design for edit post
'''
@login_required
@require_http_methods(["POST"])
def update_post(request, AUTHOR_ID, POST_ID):
    # print('edited arguemnt POST_ID', str(POST_ID))
    id = host_server + 'author/' + str(AUTHOR_ID) + '/posts/' + str(POST_ID)
    # print("edited post id:", id)
    user = None
    username=""
    if request.user.is_authenticated:
        user = request.user
        username = request.user.profile.displayName

    request_post = request.POST
    title = request_post.get("title", "")
    print("title ", title)
    description = request_post.get("description", "")
    content_type = request_post.get("contentType", "")



    f = request.FILES.get("file", "")
    print(f)
    if len(f) > 0:
        content_type = "image/" + os.path.splitext(f.name)[-1][1:]
        with f.open("rb") as image_file:
            content = base64.b64encode(image_file.read())
    else:
        content = description
    updateFlag = updatePost(id, title, description, content_type, content)
    if updateFlag:
        # print("Successful edited post, info: ", description)
        response = HttpResponse(status=200)
        return response
    else:
        print("failed to edit the post!!", description)

    response = redirect("/author/" + str(user.id) + "/my_posts/")
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
    form.fields['display_name'].initial = profile.displayName
    # form.fields['last_name'].initial = profile.displayName
    context = {}
    context['form']= form
    inbox = request.user.inbox

    friend_request_num = len(inbox.friend_requests.all())
    # print(friend_request_num)

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
        # print("new url:", url)
        display_name = post_obj["display_name"]
        # print("new name:", display_name)
        updateProfile(user.id, display_name, email, url, github)
        # print("profile id:",  str(request.user.profile.id))
        # response = redirect("author/"+ str(request.user.profile.id).split('/')[-1] + "/profile/")
        response = redirect("")
        return response




@login_required
@require_http_methods(["GET"])
@login_required
def my_friends(request,AUTHOR_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # print(cur_user_name)
    friend_list = getFriends(request.user.id)

    # print(friend_list)
    cur_author = request.user.profile
    author_num_follwers = len(cur_author.followers.items.all())
    friend_request_num = len(request.user.inbox.friend_requests.all())
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
    # print(AUTHOR_ID, FRIEND_ID)
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
    # print("---------------------------Getting user ---------------")
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
        print("Search for profile locally...")
        target = Profile.objects.get(id=target_id)
        serializer = ProfileSerializer(target)

        numberID_target = target_id.split("/")[-1]
        server_name = user.username


        # return response
        redirect_url = "../my_stream/" + server_name +"/" + numberID_target + "/"


        json_dict = {"url": redirect_url}

        return JsonResponse(json_dict, status=200)
    except Profile.DoesNotExist:
        print("Trying you get foreign profile...")
        response = profileRequest("GET", author_origin, target_id.split("/")[-1])
        #print(author_origin)
        print(response.status_code)
        print(response.json())
        numberID_target = target_id.split("/")[-1]
        server_name = user.username

        if response.status_code < 400:
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
                redirect_url = "../my_stream/" + server_name +"/" + numberID_target + "/"
                json_dict = {"url": redirect_url}
                return JsonResponse(json_dict, status=200)
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
decide to accept a friend request or not
'''
@login_required
@require_http_methods(["POST"])
def make_friend(request, AUTHOR_ID):
    data = JSONParser().parse(request)
    request_id = data['request_id']
    if data['decision'] == "accept":
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
            FriendRequest.objects.get(id=request_id).delete()
        except:
            return JsonResponse({}, status=400)
        new_friend = friend_request.actor
        request.user.profile.friends.add(new_friend)
        return JsonResponse({"accept": "true"}, status=200)

    elif data['decision'] == "reject":
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
            FriendRequest.objects.get(id=request_id).delete()
            return JsonResponse({"reject": "true"}, status=200)
        except:
            return JsonResponse({}, status=400)

'''
delete a friend
'''
@login_required
@require_http_methods(["POST"])
def unbefriend(request, AUTHOR_ID):
    data = JSONParser().parse(request)
    friend_id = data['friend_id']
    try:
        old_friend = Profile.objects.get(id=friend_id)
        user = request.user
        user.profile.friends.remove(old_friend)
        user.save()
        return JsonResponse({"unbefriend": "true"}, status=200)
    except:
        return JsonResponse({}, status=400)


'''
reshare a post
'''
@login_required
@require_http_methods(["POST"])
def reshare(request, AUTHOR_ID):
    data = JSONParser().parse(request)
    post_id = data['post_id']
    #try:
    post = Post.objects.get(id=post_id)

    source = request.user.profile.id
    origin = post.origin # who origin create
    title = post.title
    description = post.description
    content_type = post.contentType
    visibility = post.visibility
    categories = post.categories
    content = post.content
    unlisted = str(post.unlisted)
    createFlag = createPost(title, source, origin, description, content_type, content, request.user.profile, categories, visibility, unlisted, True)
    if createFlag:
        response = JsonResponse({"reshare": "true"}, status=200)
        return response
    else:
        response = JsonResponse({"reshare": "false"}, status=400)
    # response = render(request, "chat/posts.html", dynamic_contain)
    return response
    # except:
    #     return JsonResponse({}, status=400)


@login_required
@require_http_methods(["GET"])
def get_github_activity(request, AUTHOR_ID):
    try:
        token = os.getenv('GITHUB_TOKEN')
        user = User.objects.get(id=AUTHOR_ID)
        github_name = user.profile.github.split('/')[-1]
        # print(token)
        # owner = "MartinHeinz"
        # repo = "python-project-blueprint"
        # query_url = f"https://api.github.com/users/${github_name}/events"
        query_url = f"https://api.github.com/users/%s/events" %github_name
        params = {
            "state": "open",
        }
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url)
        # pprint(r.json())
        return r.json()
    except Exception as e:
        print(e)
        return None
    # pprint(r.json())


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
