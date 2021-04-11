from django.urls import path
from . import views
from . import api
# from pagedown.views import image_upload_view
# from .views import SignUpView

urlpatterns = [
    path("", views.start_homepage, name=""),

    #deign for give brother all posts
    path(r"all_posts/", api.all_posts_obj, name="all_posts_obj"),


    path("author/<str:AUTHOR_ID>/profile/", views.profile, name="profile"),
    path("author/<str:AUTHOR_ID>/", api.profile_obj, name="profile_obj"),

    path(r"author/<str:AUTHOR_ID>/my_posts/", views.posts, name="make_posts"),
    path(r"author/<str:AUTHOR_ID>/my_posts/<str:POST_ID>/edit/", views.update_post, name="update_posts"),
    
    path(r'author/<str:AUTHOR_ID>/posts/',api.posts_obj, name='make_posts_obj'),
    path(r'author/<str:AUTHOR_ID>/posts/<str:POST_ID>',api.post_obj, name='make_post_obj'),
    path(r'author/<str:AUTHOR_ID>/posts/<str:POST_ID>/comments',api.comment_list_obj, name='comment_list_obj'),

    path(r'author/<str:AUTHOR_ID>/github/',api.github_act_obj, name='github_activity_obj'),


    # show info => get request, views.public_channel originally called feed, and able to comment
    path(r"author/<str:AUTHOR_ID>/my_stream/", views.my_stream, name="my_stream"),
    path(r"author/<str:AUTHOR_ID>/my_stream/<str:SERVER>/<str:FOREIGN_ID>/", views.foreign_public_channel, name="foreign_public_channel"),

    path(r"author/<str:AUTHOR_ID>/stream/", api.stream_obj, name="stream"),




    # get search bar
    path(r"author/<str:AUTHOR_ID>/search/", views.search, name="search"),

    # path(r"author/<str:AUTHOR_ID>/my_posts/?search<str:FOREIGN_ID>", views.search_user, name="search"),

    # show friend list
    path(r"author/<str:AUTHOR_ID>/my_friends/", views.my_friends, name="my_friends"),
    # check if new friend request
    path("ifFriendRequest/", views.if_friend_request, name="if_friend_request"),

    path(r"author/<str:AUTHOR_ID>/friends/delete/<str:FRIEND_ID>/", views.delete_friend, name="friend_delete"),

    # add friend
    path(r"author/<str:AUTHOR_ID>/friends/add/<str:FRIEND_ID>/", views.add_friend, name="friend_add"),

    # path(r"author/<str:AUTHOR_ID>/friends/accept/<str:FRIEND_REQUEST_ID>/", views.accept_friend_request, name="accept_friend_request"),
    # path(r"author/<str:AUTHOR_ID>/friends/reject/<str:FRIEND_REQUEST_ID>/", views.reject_friend_request, name="reject_friend_request"),

    path(r"author/<str:AUTHOR_ID>/makefriend/", views.make_friend, name="make_friend"),
    path(r"author/<str:AUTHOR_ID>/unbefriend/", views.unbefriend, name="unbefriend"),

    path(r"author/<str:AUTHOR_ID>/reshare/", views.reshare, name="reshare"),

    # URL: ://service/author/{AUTHOR_ID}/followers/
    path(r"author/<str:AUTHOR_ID>/followers/", api.followers_obj, name="followers_obj"),
    # URL:URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    # add a follower FOREIGN to AUTHOR
    path(r"author/<str:AUTHOR_ID>/followers/<str:FOREIGN_AUTHOR_ID>", api.follower_obj, name="follower_obj"),
    # http://127.0.0.1:8000/author/6/my_stream/david/1/
    path(r"get_user/<str:SERVER>/<str:AUTHOR_ID>/", views.get_user, name="get_user"),

    #Liked
    path("author/<str:AUTHOR_ID>/liked/", api.liked_post_obj, name="like_post"),


    #follow: following a body, inside view, we need it, since we need to refresh page, or we can do it in AJAX_ js
    path(r"author/<str:AUTHOR_ID>/following/<str:SERVER>/<str:FOREIGN_ID>/", views.following,name="following_view"),



    #  Doing----------------------------------------------------------------------------------------------------

    # #follow: unfollow a body, inside view
    # ath(r"author/<str:AUTHOR_ID>/unfollow/<str:FOREIGN_AUTHOR_ID>/", views.unfollow,name="unfollow_view"),



    #TODO ---------------------------------- ----------------------------------------------------------------
    path("author/<str:AUTHOR_ID>/befriend/", api.befriend, name="befriend"),

    # friends: GET
    #(get all friends of author)
    path("author/<str:AUTHOR_ID>/friends/", api.get_friends_obj, name = "get_friends"),

    #Get likes for a Post
    path("author/<str:AUTHOR_ID>/posts/<str:POST_ID>/likes/", api.likes_post_obj, name="likes_post"),
    path("author/<str:AUTHOR_ID>/inbox", api.inbox, name="inbox"),
    path("author/<str:AUTHOR_ID>/likes", api.inbox, name="author_likes"),

    # # Get likes for a Comment
    path("author/<str:AUTHOR_ID>/posts/<str:POST_ID>/comments/<str:COMMENT_ID>/likes", api.likes_comment_obj, name="likes_post_comment"),

    # path(
    # 'pagedown/image-upload/',
    # image_upload_view,
    # name="pagedown-image-upload"),





    # TODO ----------------------------------------------------------------------------------------------------

    # # show friend list
    # path("author/<str:AUTHOR_ID>/friends/delete/<str:FRIEND_ID>/", api.delete_friend_obj, name="friend_delete"),
    # delete friend
    # # Create a Like for either a Post or a Comment
    # # This also as a side effect, sends to Inbox

    ##### path("author/<str:AUTHOR_ID>/likes/", api.likes_obj, name="likes")
    # check if new friend request
    # path("ifFriendRequest/", views.if_friend_request, name="if_friend_request"),

]




'''
Below is the dead code, or previous version, keep it , incase need that in the future
HEAD=================================>

    # handle delete
    path("home/delete<str:ID>/", views.delete, name="delete"),
    # path("feed/delete<str:ID>/", views.delete_in_feed, name="delete_post_in_feed"),

    # handle edit
    # path(r"home/edit<str:ID>/", views.edit, name="edit"),
    # path(r"feed/edit<str:ID>/", views.edit_in_feed, name="edit_in_feed"),
    # path(r"feed/edit/", views.edit_in_feed, name="edit_in_feed"),

    #path('', views.index, name='index'),
    #path('home', views.home_view, name='home')
'''
