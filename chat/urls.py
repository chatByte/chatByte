from django.urls import path
from . import views
from . import api
# from .views import SignUpView

urlpatterns = [
    path("", views.start_homepage, name=""),

    path("author/<str:AUTHOR_ID>/profile/", views.profile, name="profile"),
    path("author/<str:AUTHOR_ID>/", api.profile_obj, name="profile_obj"),

    path(r"author/<str:AUTHOR_ID>/my_posts/", views.posts, name="make_posts"),
    #
    path(r'author/<str:AUTHOR_ID>/posts/',api.posts_obj, name='make_posts_obj'),
    path(r'author/<str:AUTHOR_ID>/posts/<str:POST_ID>/',api.post_obj, name='make_post_obj'),
    path(r'author/<str:AUTHOR_ID>/posts/<str:POST_ID>/comments/',api.comment_list_obj, name='comment_list_obj'),


    # show info => get request, views.public_channel originally called feed, and able to comment
    path(r"author/<str:AUTHOR_ID>/public_channel/", views.home_public_channel, name="public_channel"),
    path(r"author/<str:AUTHOR_ID>/public_channel/<str:FOREIGN_ID>/", views.friend_public_channel, name="public_channel"),


    # handle delete
    path("home/delete<str:ID>/", views.delete, name="delete"),
    # path("feed/delete<str:ID>/", views.delete_in_feed, name="delete_post_in_feed"),

    # handle edit
    # path(r"home/edit<str:ID>/", views.edit, name="edit"),
    # path(r"feed/edit<str:ID>/", views.edit_in_feed, name="edit_in_feed"),
    # path(r"feed/edit/", views.edit_in_feed, name="edit_in_feed"),

    path(r"author/<str:AUTHOR_ID>/my_friends/", views.my_friends, name="my_friends"),
    # check if new friend request
    path("ifFriendRequest/", views.if_friend_request, name="if_friend_request"),
    # show friend list
    path(r"author/<str:AUTHOR_ID>/friends/delete/<str:FRIEND_ID>/", views.delete_friend, name="friend_delete"),

    # add friend
    path(r"author/<str:AUTHOR_ID>/friends/add/<str:FRIEND_ID>/", views.add_friend, name="friend_add"),
    path(r"author/<str:AUTHOR_ID>/friends/", views.my_friends, name="my_friends"),

    path(r"author/<str:AUTHOR_ID>/friends/accept/<str:FRIEND_REQUEST_ID>/", views.accept_friend_request, name="accept_friend_request"),
    path(r"author/<str:AUTHOR_ID>/friends/reject/<str:FRIEND_REQUEST_ID>/", views.reject_friend_request, name="reject_friend_request"),


    #followers:
    # URL: ://service/author/{AUTHOR_ID}/followers/
    path(r"author/<str:AUTHOR_ID>/followers/", api.follower_obj, name="follower_obj"),
    # URL:URL: ://service/author/{AUTHOR_ID}/followers/{FOREIGN_AUTHOR_ID}
    path(r"author/<str:AUTHOR_ID>/followers/<str:FOREIGN_AUTHOR_ID>", api.followers_obj, name="followers_obj"),


    #Liked
    path("author/<str:AUTHOR_ID>/liked/", api.liked_post_obj, name="like_post"),


    # # show friend list
    # path("author/<str:AUTHOR_ID>/friends/delete/<str:FRIEND_ID>/", api.delete_friend_obj, name="friend_delete"),
    # delete friend
    #  Doing----------------------------------------------------------------------------------------------------

    #TODO ---------------------------------- ----------------------------------------------------------------
    path("author/<str:AUTHOR_ID>/befriend/", api.befriend, name="befriend"),

    # friends: GET
    #(get all friends of author)
    path("author/<str:AUTHOR_ID>/friends/", api.get_friends_obj, name = "get_friends"),

    #Get likes for a Post
    path("author/<str:AUTHOR_ID>/posts/<str:POST_ID>/likes/", api.likes_post_obj, name="likes_post"),
    path("author/<str:AUTHOR_ID>/inbox/", api.inbox, name="likes_post"),

    # # Get likes for a Comment
    path("://service/author/<str:AUTHOR_ID>/posts/<str:POST_ID>/comments/<str:COMMENT_ID>/likes", api.likes_comment_obj, name="likes_post_comment")



    # # Create a Like for either a Post or a Comment
    # # This also as a side effect, sends to Inbox

    ##### path("author/<str:AUTHOR_ID>/likes/", api.likes_obj, name="likes")



    # TODO ----------------------------------------------------------------------------------------------------


    path("author/<str:AUTHOR_ID>/followers/<str:FOREIGN_AUTHOR_ID>/", api.follower_obj, "follower"),
    path("author/<str:AUTHOR_ID>/followers/", api.followers_obj, "followers"),
    # check if new friend request
    # path("ifFriendRequest/", views.if_friend_request, name="if_friend_request"),
  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]
