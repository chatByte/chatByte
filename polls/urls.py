"""
This is the polls/url.py file

This file only gets consulted by Django if the URL starts with
localhost:8080/polls/
it defines what django should do for anything after that
"""

from django.urls import path
from . import views

#  first version
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'), # localhost:8080/polls/ + ""
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]
#  second version
# app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]