from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


"""
REST Author, Generate response at my profile page ,
"""
# @login_required
def profile_obj(request):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    author = request.user.profile

    obj = {
    "type":"author",
    # ID of the Author
    "id": author.URL,
    # the home host of the author
    "host": author.HOST,
    # the display name of the author
    "displayName": author.DISPLAY_NAME,
    # url to the authors profile
    "url": author.URL,
    # HATEOS url for Github API
    "github": author.GITHUB
    }


    # query to database
    if request.method == "GET":
        return  json.dumps(obj)
    elif request.method == "POST":

        post_obj = json.loads(request.body)
        url = post_obj["url"]
        displayName = post_obj["displayName"]
        github = post_obj["github"]
        # we do not allowed leave our server
        # host = post_obj["host"]
        updateProfile(displayName, url, github)
        return post_obj

# coment views.py
@require_http_methods(["GET", "POST"])
def comments_obj(request, AUTHOR_ID, POST_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    if request.method == "GET":
        comments = getComments(POST_ID)

        # TODO return objects or html?
        return comments
    elif request.method == "POST":
        request_post = request.POST
        author = request_post.get("author")
        contentType = request_post.get("contentType")
        comment = request_post.get("comment")
        createComment(author, comment, contentType)
        return request_post


@require_http_methods(["GET"])
def delete_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True

def add_friend_obj(request, AUTHOR_ID, FRIEND_ID):
    return True


@login_required
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def post_obj(request, AUTHOR_ID, POST_ID):
    cur_user_name = None
    if request.user.is_authenticated:
        cur_user_name = request.user.username
    # post_id = request.build_absolute_uri().split("/")[-2][6:]

    if request.method == "DELETE":
        deletePost(POST_ID)
        response = redirect("../posts/")
        return response
    elif request.method == "GET":
        post = getPost(POST_ID)
        # TODO return an object or html?
        return post
    elif request.method == "POST":
        # updatePost()
        pass

def posts_obj():
    pass