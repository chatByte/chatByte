from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path("signup/", views.signup, name="signup"),
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



  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]
