from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path("login/", views.login, name='login'),
  path("signup/", views.signup, name="signup"),
  path("mystream/", views.my_timeline, name="my_timeline"),
  path("seeothers/", views.others_timeline, name="others_timeline"),
  path("feed/", views.make_post, name="feed"),
  path("profile/", views.profile, name="profile"),
  #path('', views.index, name='index'),
  #path('home', views.home_view, name='home')
]