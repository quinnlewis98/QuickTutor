from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    return render(request, 'app/index.html')


def redirect(request):
    return render(request, 'app/redirect.html')


def feed(request):
    requests_list = Request.objects.order_by('-pub_date')[:]
    # process each request in a for loop
    context = {
        'requests_list': requests_list,
    }
    return render(request, 'app/feed.html', context)


def myRequest(request):
    return render(request, 'app/myRequest.html')


def profile(request):
    return render(request, 'app/profile.html')


def contacts(request):
    return render(request, 'app/contacts.html')


def messages(request):
    return render(request, 'app/messages.html')


