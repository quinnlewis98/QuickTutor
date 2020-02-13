from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("let's get this money (this is the app index)")