from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import *
from .forms import *



def index(request):
    if request.user.is_authenticated:
        return render(request, 'app/redirect.html')
    else:
        return render(request, 'app/index.html')


def redirect(request):
    if request.user.is_authenticated:
        return render(request, 'app/redirect.html')
    else:
        return HttpResponseRedirect('/')


def feed(request):
    if request.user.is_authenticated:
        requests_list = Request.objects.order_by('-pub_date')[:]
        # process each request in a for loop
        context = {
            'requests_list': requests_list,
        }
        return render(request, 'app/feed.html', context)
    else:
        return HttpResponseRedirect('/')



def myRequest(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            location = request.POST['location']
            description = request.POST['description']
            new_request = Request()
            new_request.title = title
            new_request.location = location
            new_request.description = description
            new_request.pub_date = timezone.now()
            new_request.user = request.user.username
            new_request.save()
            print("request saved")
        return render(request, 'app/myRequest.html')
    else:
        return HttpResponseRedirect('/')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'app/profile.html')
    else:
        return HttpResponseRedirect('/')


def contacts(request):
    if request.user.is_authenticated:
        return render(request, 'app/contacts.html')
    else:
        return HttpResponseRedirect('/')

def messages(request):
    if request.user.is_authenticated:
        return render(request, 'app/messages.html')
    else:
        return HttpResponseRedirect('/')

