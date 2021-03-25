from django.urls import path
from . import views
# from .views import SignUpView

urlpatterns = [
    # path('login/', views.login, name='login'),
    # path("accounts/signup/", SignUpView.as_view(), name="signup"),
    # path("home/", views.home, name="home"),
    path("", views.start_homepage, name=""),
    path("friend/", views.friend_profile, name="friend_profile"),
    # path("author/<str:AUTHOR_ID>/feed", views.make_post, name="feed"),

    path("author/<str:AUTHOR_ID>/", views.profile, name="profile"),
    # path("author/<str:AUTHOR_ID>/", views.profile_obj, name="profile_obj"),

    path(r'author/<str:AUTHOR_ID>/posts/',views.make_posts, name='make_post'),
    path(r'author/<str:AUTHOR_ID>/posts/<str:POST_ID>/',views.make_post, name='make_post'),


    # show info => get request, views.public_channel originally called feed, and able to comment
    path(r"author/<str:AUTHOR_ID>/public_channel/", views.home_public_channel, name="public_channel"),


    # handle delete
    # path("home/delete<str:ID>/", views.delete, name="delete"),
    # path("feed/delete<str:ID>/", views.delete_in_feed, name="delete_post_in_feed"),

    # handle edit
    path(r"home/edit<str:ID>/", views.edit, name="edit"),
    path(r"feed/edit<str:ID>/", views.edit_in_feed, name="edit_in_feed"),
    # path(r"feed/edit/", views.edit_in_feed, name="edit_in_feed"),

    path("author/<str:AUTHOR_ID>/friends/<str:FRIEND_ID>/", views.my_friends, name="my_friends"),

    # show friend list
    path("author/<str:AUTHOR_ID>/friends/delete/<str:FRIEND_ID>/", views.delete_friend, name="friend_delete"),

    # add friend
    path("author/<str:AUTHOR_ID>/friends/add/<str:FRIEND_ID>", views.add_friend, name="friend_add"),

    # delete friend

  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]
