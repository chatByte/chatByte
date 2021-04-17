from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import *
from .serializers import *
from .backend import *
import os
from .remoteProxy import *
from .signals import host as host_server
import json

import requests
import os
from pprint import pprint



class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


'''
Design for giving our brother all posts, since we love each other
'''
# No CSRF token
@csrf_exempt
# methdo
@api_view(['GET'])
# which AUTH using right now
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
# permission, -> auth
@permission_classes([IsAuthenticated])
def all_posts_obj(request):
    if request.method == 'GET':
        posts = Post.objects
        # print(posts.all())
        posts = posts.order_by('-published')

        # serializer = PostSerializer(posts, many=True)
        
        # pagination
        pagination = PageNumberPagination()
        paginated_results = pagination.paginate_queryset(posts.all(), request)

        serializer = PostSerializer(paginated_results, many=True)

        next_link = pagination.get_next_link()
        if next_link == None:
            next_link = ""
        
        prev_link = pagination.get_previous_link()

        if prev_link == None:
            prev_link = ""

        data = {
            'count': pagination.page.paginator.count,
            'next': next_link,
            'previous': prev_link,
            'posts': serializer.data,
        }
        return JsonResponse(data, safe=False)

    



'''
Design for give one post API 
'''
# No CSRF token
@csrf_exempt
# methdo
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
# which AUTH using right now
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
# permission, -> auth
@permission_classes([IsAuthenticated])
def post_obj(request, AUTHOR_ID, POST_ID):

    USER_ID = (AUTHOR_ID + '.')[:-1]
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    USER_POST_ID = POST_ID
    POST_ID = AUTHOR_ID + "/posts/" + POST_ID
    server_origin = request.META.get("HTTP_X_SERVER")

    if server_origin is not None and server_origin != host_server:
        return postRequest(request.method,server_origin, USER_ID, USER_POST_ID, request.data)
    else:
        if request.method == "DELETE":
            # remove the post
            try:
                Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                print("post does not exist")
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            deletePost(POST_ID)
            return JsonResponse({'status':'true','message':'successful'}, status=204)
        elif request.method == "GET":
            # get the public post
            try:
                post = Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            serializer = PostSerializer(post)
            return JsonResponse(serializer.data)
        elif request.method == 'POST':
            # update the post
            try:
                post = Post.objects.get(id=POST_ID)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
            data = JSONParser().parse(request)
            serializer = PostSerializer(post, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        elif request.method == 'PUT':
            # create a post with that post_id
            try:
                post = Post.objects.get(id=POST_ID)
                return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' already exists'}, status=409)
            except Post.DoesNotExist:
                pass
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)



"""
design for get a list of posts
"""
#author/<str:AUTHOR_ID>/posts/'
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def posts_obj(request, AUTHOR_ID):

    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return postsRequest(request.method,server_origin, USER_ID, request.data)
    else:
        if request.method == 'GET':
            profile = Profile.objects.get(id=AUTHOR_ID)
            posts = profile.timeline
            
            posts = posts.filter(author=profile).order_by('-published')

            # pagination
            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(posts.all(), request)

            serializer = PostSerializer(paginated_results, many=True)

            next_link = pagination.get_next_link()
            if next_link == None:
                next_link = ""
            
            prev_link = pagination.get_previous_link()

            if prev_link == None:
                prev_link = ""

            data = {
                'count': pagination.page.paginator.count,
                'next': next_link,
                'previous': prev_link,
                'posts': serializer.data,
            }
            return JsonResponse(data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = PostSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                post = serializer.save()
                post.author.timeline.add(post)
                post.author.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)




'''
Tetsing format:
http://127.0.0.1:8000/chat/author/1/posts/3d93a8ea-3175-4e75-b1ae-03655c663b75/comments/

{
    "type":"comment",
      "author":{
        "type":"author",
        "id":1,
        "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
          "host":"http://127.0.0.1:5454/",
          "displayName":"Greg Johnson",
          "github": "http://github.com/gjohnson"
    },
    "comment":"Sick Olde English",
    "contentType":"text/markdown",
    "published":"2015-03-09T13:07:04+00:00",
    "id":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
}

'''
"""
get a list of comment 
"""
@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def comment_list_obj(request, AUTHOR_ID, POST_ID):
    '''
    Get conmments  for a Post
    Response Object Structure: [list of Like objects] using json
    '''

    # ex. equest.META[origin] == ("https:\\chatbyte"):
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    USER_POST_ID = (POST_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    POST_ID = host_server + "author/" + USER_ID + "/posts/" + POST_ID

    if server_origin is not None and server_origin != host_server:
        return commentRequest(request.method,server_origin, USER_ID, USER_POST_ID, request.user.id, request.data)
    else:
        # checking, comments' father exist or not
        try:
            post = Post.objects.get(id=POST_ID)
        except Post.DoesNotExist:
            return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
        if request.method == 'GET':
            # list obj contain a list of comment
            comments = post.comments
            serializer = CommentSerializer(comments, many=True)
            # pagination
            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(comments.all(), request)

            serializer = CommentSerializer(paginated_results, many=True)

            next_link = pagination.get_next_link()
            if next_link == None:
                next_link = ""
            
            prev_link = pagination.get_previous_link()

            if prev_link == None:
                prev_link = ""

            data = {
                'count': pagination.page.paginator.count,
                'next': next_link,
                'previous': prev_link,
                'comments': serializer.data,
            }
            return JsonResponse(data, safe=False)

        elif request.method == 'POST':
            # cretate comment
            data = JSONParser().parse(request)

            profile_url = request.META.get("HTTP_X_REQUEST_USER")
            origin_server = profile_url.split('author/')[0]
            author_id = profile_url.split('author/')[-1]
            try:
                author = Profile.objects.get(id=profile_url)
            except:
                try:
                    # if the author's id is not a full url, try this
                    author = Profile.objects.get(id=author_id)
                except:
                    res = profileRequest("GET", origin_server, author_id)
                    if res.status_code >= 400:
                        return JsonResponse({"Error": "Profile get failed"}, status=404)
                    author_ser = ProfileSerializer(data=res.json())
                    if author_ser.is_valid():
                        author = author_ser.save()
            comment = createComment(author, POST_ID, data['content'], data['contentType'])
            if comment:
                serializer = CommentSerializer(comment)
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse({"Error": "can't create comment properly"}, status=400)



'''
Tetsing format:
  "author":{
    "type":"author",
    "id":1,
    "url":"http://127.0.0.1:5454/author/1d698d25ff008f7538453c120f581471",
    "host":"http://127.0.0.1:5454/",
    "displayName":"Greg Johnson",
    "github": "http://github.com/gjohnson"
}
'''

"""
design for get a profile
"""
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile_obj(request, AUTHOR_ID):
    """
    REST Author, Generate response at my profile page ,
    """

    # ex. equest.META[origin] == ("https:\\chatbyte"):
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return profileRequest(request.method,server_origin, USER_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        # query to database
        if request.method == "GET":
            serializer = ProfileSerializer(profile)
            return JsonResponse(serializer.data, status=200)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)






'''
Design for get a follower obj
URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PUT', 'GET', 'DELETE'])
def follower_obj(request, AUTHOR_ID, FOREIGN_AUTHOR_ID):
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    FOREIGN_USER_ID = (FOREIGN_AUTHOR_ID + '.')[:-1]

    try:
        FOREIGN_AUTHOR_ID = server_origin + "author/" + FOREIGN_AUTHOR_ID
    except:
        FOREIGN_AUTHOR_ID = host_server + "author/" + FOREIGN_AUTHOR_ID


    if server_origin is not None and server_origin != host_server:
        res = followerRequest(request.method,server_origin, USER_ID, FOREIGN_USER_ID, request.data)
        return JsonResponse(res.json(), status=res.status_code)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=USER_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)


        if (request.method == "GET"):
            # reponse a status
            # check if follower
            try:
                print("Searching foreign author id: ", FOREIGN_AUTHOR_ID)
                try:
                    follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)
                except:
                    return JsonResponse({'status':'false','message':'FOREIGN_AUTHOR_ID: ' + FOREIGN_AUTHOR_ID + ' does not exists'}, status=404)
                if follower in profile.followers.items.all():
                    serializer = ProfileSerializer(follower)
                    return JsonResponse({'detail':'true'}, status=200)
                else:
                    return JsonResponse({'detail':'false'}, status=200)
            except Post.DoesNotExist:
                return JsonResponse({'status':'false','message':'FOREIGN_AUTHOR_ID: ' + FOREIGN_AUTHOR_ID + ' does not exists'}, status=404)

        elif (request.method == "PUT"):
            print("Putting to followers: ", FOREIGN_AUTHOR_ID)
            #add a follower , with FOREIGN_AUTHOR_ID
            foreign_author = request.META.get("HTTP_X_REQUEST_USER")
            try:
                follower = Profile.objects.get(id=foreign_author)
            except:
                foreign_server = foreign_author.split('author/')[0]
                foreign_id = foreign_author.split('author/')[1]
                headers = {"X-Server": foreign_server}
                url = str(host_server) + "author/" + str(foreign_id)
                response = requests.get(url, headers=headers, auth=HTTPBasicAuth(request.user.username, request.user.first_name))
                profile_ser = ProfileSerializer(data=response.data)
                if profile_ser.is_valid():
                    follower = profile_ser.save()
            profile.followers.items.add(follower)
            return JsonResponse({'detail': 'true'}, status=201)
            # return JsonResponse(serializer.errors, status=400)

        elif request.method == "DELETE":
            follower = Profile.objects.get(id=FOREIGN_AUTHOR_ID)
            profile.followers.items.remove(follower)
            return JsonResponse({"status": "true"}, status=200)

        return JsonResponse({"Error": "Bad request"}, status=400)




'''
# URL: ://service/author/{AUTHOR_ID}/followers/
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def followers_obj(request, AUTHOR_ID):
    # ex. equest.META[origin] == ("https:\\chatbyte"):
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")

    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return followersRequest(request.method,server_origin, USER_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        followers = profile.followers.items.all()
        serializer = ProfileSerializer(followers, many=True)
        if request.method == "GET":
            return JsonResponse({"type": "followers", "items": serializer.data}, status=200, safe=False)

        return JsonResponse(serializer.errors, status=400)






"""
design for get friends 
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_friends_obj(request, AUTHOR_ID):
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")

    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return friendsRequest(request.method,server_origin, USER_ID, request.data)
    else:
        try:
            profile = Profile.objects.get(id=AUTHOR_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)

        friends = profile.friends
        serializer = ProfileSerializer(friends, many=True)
        if request.method == "GET":
            return JsonResponse({"type": "friends", "items": serializer.data}, status=200, safe=False)

        return JsonResponse(serializer.errors, status=400)



"""
design for befriend 
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
# out box friend request, ie. accept a friend requst for box
def befriend(request, AUTHOR_ID):
    data = JSONParser().parse(request)

    serializer = ProfileSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        friend_id = data['id']
        try:
            friend = Profile.objects.get(id=friend_id)
        except:
            serializer.save()
            friend = Profile.objects.get(id=friend_id)
        profile = Profile.objects.get(pk=AUTHOR_ID)
        profile.friends.add(friend)
        profile.friends.save()
        return JsonResponse(data, status=200)
    return JsonResponse(serializer.errors, status=400)





'''
Get likes for a Post
Response Object Structure: [list of Like objects]
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def likes_post_obj(request, AUTHOR_ID, POST_ID):
    USER_ID = (AUTHOR_ID + '.')[:-1]
    USER_POST_ID = (POST_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    POST_ID = host_server + "author/" + USER_ID + "/posts/" + POST_ID

    if server_origin is not None and server_origin != host_server:
        return likesRequest(request.method, server_origin, USER_ID, USER_POST_ID, request.data)
    else:
        try:
            post = Post.objects.get(pk=POST_ID)
        except Post.DoesNotExist:
            return JsonResponse({'status':'false','message':'post id: ' + POST_ID + ' does not exists'}, status=404)
        likes = post.likes
        serializer = LikeSerializer(likes, many=True)
        # if serializer.is_valid(raise_exception=True):
        return JsonResponse(serializer.data, status=200, safe=False)



"""
deisgn for like a signle comment
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def likes_comment_obj(request, AUTHOR_ID, POST_ID, COMMENT_ID):
    # req_origin = request.META["Origin"]
    USER_ID = (AUTHOR_ID + '.')[:-1]
    USER_POST_ID = (POST_ID + '.')[:-1]
    USER_COMMENT_ID = (COMMENT_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")

    AUTHOR_ID = host_server + "author/" + AUTHOR_ID
    POST_ID = host_server + "author/" + USER_ID + "/posts/" + POST_ID
    COMMENT_ID = POST_ID + "/comments/" + COMMENT_ID

    if server_origin is not None and server_origin != host_server:
        return commentLikesRequest(request.method, server_origin, USER_ID, USER_POST_ID, USER_COMMENT_ID, request.data)
    else:
        try:
            comment = Comment.objects.get(pk=COMMENT_ID)
        except Comment.DoesNotExist:
            return JsonResponse({'status':'false','message':'comment id: ' + COMMENT_ID + ' does not exists'}, status=404)
        likes = comment.likes
        serializer = LikeSerializer(likes, many=True)
        # if serializer.is_valid(raise_exception=True):
        return JsonResponse(serializer.data, status=200, safe=False)




"""
deisgn for like a signle post
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def liked_post_obj(request, AUTHOR_ID):
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return likedRequest(request.method,server_origin, USER_ID, request.data)
    else:
        # can be optimized
        try:
            profile = Profile.objects.get(user_id=USER_ID)
        except Profile.DoesNotExist:
            return JsonResponse({'status':'false','message':'user id: ' + AUTHOR_ID + ' does not exists'}, status=404)
        liked = profile.liked
        serializer = LikedSerializer(liked)
        return JsonResponse(serializer.data, status=200)


'''
# Inbox has a one-to-one relationship with User, and the User id is an integer, AUTHOR_ID
# to avoid Reference problem , make a copy of AUTHOR_ID by creating a new string

URL: ://service/author/{AUTHOR_ID}/inbox
GET: if authenticated get a list of posts sent to {AUTHOR_ID}
POST: send a post to the author
    if the type is “post” then add that post to the author’s inbox
    Here folllow is equal to be a friend request
    if the type is “follow” then add that follow is added to the author’s inbox to approve later
    if the type is “like” then add that like to the author’s inbox
DELETE: clear the inbox
'''
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET', 'DELETE'])
def inbox(request, AUTHOR_ID):
    USER_ID = (AUTHOR_ID + '.')[:-1]
    server_origin = request.META.get("HTTP_X_SERVER")
    AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        res = inboxRequest(request.method,server_origin, USER_ID, request.data)
        return JsonResponse(res.json(), status=res.status_code)
    else:
        if request.method == "POST":
            user = User.objects.get(pk=USER_ID)
            data = request.data
            if data['type'] == "post":
                return JsonResponse(data, status=200)
            elif data['type'].lower() == 'like':
                post_url = data['object'].split("/")
                # like post
                if len(post_url) == 7:
                    user_id = post_url[-3]
                    post_id = host_server + 'author/' + USER_ID + '/posts/' + post_url[-1]
                    if user_id != USER_ID:
                    # if user_id != AUTHOR_ID: # Now AUTHOR_ID is http://our-host-name/USER_ID
                        return JsonResponse({"Error": "Author id is inconsistent"}, status=404)
                    try:
                        like = Like.objects.get(id=data['id'])
                    except:
                        serializer = LikeSerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            like = serializer.save()
                        else:
                            return JsonResponse(serializer.errors, status=400)
                    try:
                        post = Post.objects.get(id=post_id)
                        post.likes.add(like)
                        post.save()
                        user.inbox.like_inbox.add(like)
                        user.save()
                        return JsonResponse(data, status=200)
                    except:
                        return JsonResponse({"Error": "Post does not exist"}, status=404)
                    
                #like comment
                elif len(post_url) == 9:
                    user_id = post_url[4]
                    # post_id = post_url[6]
                    post_id = host_server + 'author/' + user_id + '/posts/' + post_url[6]

                    # comment_id = post_url[8]
                    comment_id = host_server + 'author/' + user_id + '/posts/' + post_url[6] + '/comments/' + post_url[8]
                    # if user_id != AUTHOR_ID:
                    if user_id != USER_ID:
                        return JsonResponse({"Error": "Author id is inconsistent"}, status=404)
                    try:
                        like = Like.objects.get(id=data['id'])
                    except:
                        serializer = LikeSerializer(data=data)
                        if serializer.is_valid(raise_exception=True):
                            like = serializer.save()
                        else:
                            return JsonResponse(serializer.errors, status=400)
                    try:
                        comment = Comment.objects.get(id=comment_id)
                        comment.likes.add(like)
                        comment.save()
                        return JsonResponse(data, status=200)
                    except:
                        return JsonResponse({"Error": "comment does not exist"}, status=404)
                    
                    

            elif data['type'].lower() == 'follow':
                serializer = FriendReuqestSerializer(data=data)
                if serializer.is_valid(raise_exception=True):

                    actor_dict = data['actor'] 

                    try:
                        actor = Profile.objects.get(id=actor_dict['id'])
                    except Profile.DoesNotExist:
                        actor_serializer = ProfileSerializer(data=actor_dict)
                        if actor_serializer.is_valid(raise_exception=True):
                            actor = actor_serializer.save()

                    object_dict = data['object'] 

                    try:
                        object = Profile.objects.get(id=object_dict['id'])
                    except Profile.DoesNotExist:
                        return JsonResponse({"Error": "object does not exist"}, status=404)
                    friend_req = serializer.save(actor=actor, object=object)

                    # -----------------
                    # add to object's inbox
                    object.user.inbox.friend_requests.add(friend_req)
                    # -----------------
                    user.inbox.save()
                    return JsonResponse(data, status=200)
                return JsonResponse(serializer.errors, status=400)

            else:
                return JsonResponse({"Error": "Invalid inbox type"}, status=400)

        elif request.method == "DELETE":
            user = User.objects.get(pk=USER_ID)
            user.inbox.post_inbox.items.clear()
            user.inbox.post_inbox.save()
            user.inbox.friend_requests.clear()
            user.inbox.like_inbox.clear()
            user.inbox.save()
            return JsonResponse({}, status=204)

        elif request.method == "GET":
            user = User.objects.get(pk=USER_ID)
            post_inbox = user.inbox.post_inbox
            serializer = PostInboxSerializer(post_inbox)
            return JsonResponse(serializer.data, status=200)


"""
design for get all posts that are allowed them to see from the reqested user, which are allowed for the user required
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def stream_obj(request, AUTHOR_ID):
    server_origin = request.META.get("HTTP_X_SERVER")
    origin_server = request.META.get("HTTP_ORIGIN")
    if origin_server is not None and origin_server not in host_server:
        AUTHOR_ID = origin_server + "author/" + AUTHOR_ID
    else:
        AUTHOR_ID = host_server + "author/" + AUTHOR_ID

    if server_origin is not None and server_origin != host_server:
        return likedRequest(request.method,server_origin, AUTHOR_ID, request.data)
    else:
        if request.method == 'GET':
            try:
                posts_result = Post.objects.filter(visibility='public').filter(unlisted=False)
                try:
                    profile = Profile.objects.get(id=AUTHOR_ID)

                    for user in User.objects.all():
                        try:
                            user_friends = list(user.profile.friends.all())
                            if profile in user_friends:
                                friend_posts = user.profile.timeline.filter(visibility='friend')
                                posts_result = posts_result | friend_posts

                        except BaseException as e:
                            print(e)
                
                except BaseException as e:
                    print(e)
                
            except BaseException as e:
                print(e)
                posts_result = []
            # Get posts that's visible to the author

            pagination = PageNumberPagination()
            paginated_results = pagination.paginate_queryset(posts_result, request)

            serializer = PostSerializer(paginated_results, many=True)

            next_link = pagination.get_next_link()
            if next_link == None:
                next_link = ""
            
            prev_link = pagination.get_previous_link()

            if prev_link == None:
                prev_link = ""

            data = {
                'count': pagination.page.paginator.count,
                'next': next_link,
                'previous': prev_link,
                'posts': serializer.data,
            }
            return JsonResponse(data, safe=False)


"""
design for get github activites
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def github_act_obj(request, AUTHOR_ID):
    try:
        token = os.getenv('GITHUB_TOKEN')
        user = User.objects.get(id=AUTHOR_ID)
        github_name = user.profile.github.split('/')[-1]

        query_url = f"https://api.github.com/users/%s/events" %github_name
        params = {
            "state": "open",
        }
        headers = {'Authorization': f'token {token}'}
        r = requests.get(query_url)
        pprint(r.json())
        return JsonResponse(r.json(), status=200, safe=False)
    except Exception as e:
        print(e)
        return None
   


"""
design for inbox_likes
"""
@csrf_exempt
@authentication_classes([CsrfExemptSessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def inbox_likes(request, AUTHOR_ID):
    data = request.data
    print("Inbox likes data: ", data)
    print("")
    print("request.META.")
    print(request.META)
    
    if data['type'] == 'like':
        # from our own server
        # send the like object to remote server
        return inbox(request, AUTHOR_ID)
    foreign_author = request.META.get("HTTP_X_REQUEST_USER")


    try:
        author = Profile.objects.get(id=foreign_author)
    except:

        # return error message        
        print("X-request-user: ", foreign_author)
        if foreign_author == None:
            return JsonResponse({"error": "X-request-user is empty, plz dont send NONE, it is scary"}, safe=False, status=404)

        foreign_server = foreign_author.split('author/')[0]
        foreign_id = foreign_author.split('author/')[1]
        headers = {'Origin': host_server, 'X-Request-User': str(host_server) + "author/" + str(AUTHOR_ID), 'Content-type': 'application/json'}
        url = str(foreign_server) + "author/" + str(foreign_id)
        node = User.objects.get(last_name=foreign_server)
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(node.username, node.first_name))
        print("Profile data from remote server: ", response.json())
        profile_ser = ProfileSerializer(data=response.json())
        if profile_ser.is_valid():
            author = profile_ser.save()
    if data['type'] == 'comment':
        original_author_id = data['id'].split('author/')[1].split('/posts')[0]
        print("original author id for the liked object: ", original_author_id)
        # create a like object for comment
        like = Like.objects.create(author=author, object=data['id'], summary= author.displayName + " Likes a comment")
        # send the like to inbox directly
        data = LikeSerializer(like).data
        url = str(host_server) + "author/" + str(original_author_id) + "/inbox"
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(request.user.username, request.user.first_name))
        if response.status_code == 200:
            return JsonResponse(data, safe=False, status=201)
        return JsonResponse(data, safe=False, status=response.status_code)
    elif data['type'] == 'post':
        original_author_id = data['id'].split('author/')[1].split('/posts')[0]
        print("original author id for the liked object: ", original_author_id)
        # create a like object for post
        like = Like.objects.create(author=author, object=data['id'], summary= author.displayName + " Likes a post")
        # send the like to inbox directly
        data = LikeSerializer(like).data
        url = str(host_server) + "author/" + str(original_author_id) + "/inbox"
        headers = {'Content-type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=HTTPBasicAuth(request.user.username, request.user.first_name))
        if response.status_code == 200:
            return JsonResponse(data, safe=False, status=201)
        return JsonResponse(data, safe=False, status=response.status_code)
    else:
        return JsonResponse({"Detail": "Invalid like type"}, safe=False, status=400)