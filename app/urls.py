from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect/', views.redirect, name='redirect'),
    path('feed/', views.feed, name='feed'),
    path('myRequest/', views.myRequest, name='myRequest'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
    path('messages/', views.messages, name='messages'),
]