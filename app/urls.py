from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect/', views.redirect, name='redirect'),
    path('feed/', views.feed, name='feed'),
    path('myRequest/', views.myRequest, name='myRequest'),
]