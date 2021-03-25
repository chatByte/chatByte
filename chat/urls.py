from django.urls import path
from . import views
# from .views import SignUpView

urlpatterns = [
    # path('login/', views.login, name='login'),
    # path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("home/", views.home, name="home"),
    path("friend/", views.friend_profile, name="friend_profile"),

    path("feed/", views.make_post, name="feed"),
    path("profile/", views.profile, name="profile"),
    path(r'feed/make_post/',views.make_post, name='make_post'),

    # handle delete
    path("home/delete<str:ID>/", views.delete, name="delete"),
    path("feed/delete<str:ID>/", views.delete_in_feed, name="delete_post_in_feed"),

    # handle edit
    path(r"home/edit<str:ID>/", views.edit, name="edit"),
    path(r"feed/edit<str:ID>/", views.edit_in_feed, name="edit_in_feed"),
    # path(r"feed/edit/", views.edit_in_feed, name="edit_in_feed"),

    # view all my friends
    path("myFriends/", views.my_friends, name="my_friends"),


  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]
