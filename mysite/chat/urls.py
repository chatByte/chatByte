from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login, name='login'),
  path("signup/", views.signup, name="signup"),
  path("home/", views.home, name="home"),
  path("friend/", views.friend_profile, name="friend_profile"),
  path("feed/", views.make_post, name="feed"),
  path("profile/", views.profile, name="profile"),
  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]