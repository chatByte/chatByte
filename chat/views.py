from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse


from .form import *
from .backend import *
import base64
import os
import json



"""
views.py receive request and create repose to client,
Create your views here.
"""

# #class based view
# class SignUpView(generic.CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'


"""
Generate response at login page
"""
# def login(request):
#     context = {}
#     context['form']= UserForm()
#     if request.method == "GET":
#         return render(request, "chat/login.html", context)
#     elif request.method == "POST":
#         username = None
#         if request.user.is_authenticated:
#             username = request.user.username
#             cur_user_name = username
#             response = redirect("/chat/home")
#             return response
#         else:
#             messages.error(request, "Invalid user name or password!")
#             response = render(request, 'chat/login.html', context)
#             return response

# """
# Generate response at signup page

# """

# def signup(request):
#     context = {}
#     context['UserForm'] = UserForm()
#     context['ProfileForm'] = ProfileForm()
#     response = render(request, "chat/signup.html", context)
#     if request.method == "GET":
#         return response
#     elif request.method == "POST":
#         url = request.POST.get("URL")

#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         github = request.POST.get("GITHUB")

#         # password = request.POST.get("Password")
#         # retype_password = request.POST.get("Retype_password")
#         host = request.POST.get("HOST")
#         # first method to handle user name exist, can be optimize later
#         if validActor(username, password):
#             messages.error(request, 'User name exists!')
#             return response
#         else:
#             if retype_password != password:
#                 messages.error(request, 'Password does not match!')
#                 return response
#             createAuthor(host, username, url, github)
#             createActor(username, password)
#             cur_user_name = username
#             response = redirect("/chat/home/")
#             return response

#         # second method to handle user name exist, can be optimize later
#         if createAuthor("this", username, url, github):
#           return redirect("/chat/profile/")
#         else:
#           messages.error(request, 'User name exists!')
#           return render(request, "chat/signup.html", context)

@login_required
def start_homepage(request):
    if request.user.is_authenticated:
        return redirect("/chat/author/" + str(request.user.id) + "/profile/")




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

        return redirect('/chat/author/' + str(user.id))
    return render(request, 'registration/signup.html', {'form': form})



"""
Generate response at home page  => eveyones' post here
"""
# get feed and
# post: comment/like => send post request to host server(edit post function),
@require_http_methods(["GET", "POST"])
@login_required
def home_public_channel(request, AUTHOR_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    cur_author = request.user
    # a list of post
    mytimeline = cur_author.profile.timeline.all() #getTimeline(cur_user_name)

    author_num_follwers = len(cur_author.profile.followers.all())

    dynamic_contain = {
        'myName' : cur_author.profile.displayName,
        'timeline': mytimeline,
        'author_num_follwers': author_num_follwers

    }

    # for user in User.objects.all():
    #     Token.objects.get_or_create(user=user)


    response = render(request, "chat/home.html", dynamic_contain)

    if request.method == "GET":

        return response
    elif request.method == "POST":

        # change later
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

    author_num_follwers = len(cur_author.profile.followers.all())

    dynamic_contain = {
        'myName' : cur_author.profile.displayName,
        'timeline': mytimeline,
        'author_num_follwers': author_num_follwers,
        'isFriend': isFriend,
        'myId':cur_author.id

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
    mytimeline = cur_author.timeline.all() #getTimeline(cur_user_name)
    author_num_follwers = len(cur_author.followers.all())


    dynamic_contain = {
        'fullName':'Ritsu Onodera',
        'author_num_follwers': author_num_follwers,
        'test_name': cur_user_name,
        'myName' : cur_author.displayName,
        'timeline': mytimeline

    }

    # Get the current pages' author

    if request.method == "GET":
        response = render(request, "chat/posts.html", dynamic_contain)
        return response

    elif request.method == "POST":

        request_post = request.POST
        title = request_post.get("title", "")
        source = cur_user_name # Who share it to me
        origin = cur_user_name # who origin create
        description = request_post.get("description", "")
        content_type = request_post.get("contentType", "")
        f = request.FILES.get("file", "")
        categories = "text/plain" # web, tutorial, can be delete  # ?? dropdown
        visibility = request_post.get("visibility", "")

        if len(f) > 0:
            categories = "image/" + os.path.splitext(f.name)[-1][1:]
            with f.open("rb") as image_file:
                content = base64.b64encode(image_file.read())
        else:
            content = description

        createFlag = createPost(title, source, origin, description, content_type, content, request.user, categories, visibility)
        if createFlag:
            print("haha, successful create post, info: ", description)
            response = redirect("/chat/author/"+ str(AUTHOR_ID) + "/public_channel/")
            return response
        else:
            print("server feels sad ", description)

        response = render(request, "chat/posts.html", dynamic_contain)
        return response


"""
Generate response ,when delete user at feed page ,
"""
# only allowed DELETE or POST to delete feed's post
# @login_required
# @require_http_methods(["DELETE", "POST"])
# def delete_in_feed(request, ID):
#     cur_user_name = None
#     if request.user.is_authenticated:
#         cur_user_name = request.user.username
#     # post_id = request.build_absolute_uri().split("/")[-2][6:]

#     deletePost(ID)
#     response = redirect("/chat/feed/")

#     return response


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
        response = redirect("/chat/author/"+ str(request.user.id) + "/profile/")
        return response





# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })

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
    response = redirect("/chat/author/"+ str(request.user.id) + "/public_channel/")
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
    author_num_follwers = len(cur_author.followers.all())

    dynamic_contain = {
        'myName' : cur_author.displayName,
        'friend_list': friend_list,
        'author_num_follwers': author_num_follwers,
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
    except BaseException as e:
        print(e)
        return False
    return redirect('/chat/author/'+str(request.user.id)+'/friends/')

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
        return False
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
        if all_friend_request:
            newest = all_friend_request.reverse()[0]
            data = {}
            data['friend'] = newest.author.profile.displayName
            data['id'] = newest.id

            # return the newest friend request's name
            return JsonResponse(data)

        else:
            return HttpResponse(status=304)

    except BaseException as e:
        print(e)
        return HttpResponse(status=304)
