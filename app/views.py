from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth import get_user
from django.contrib.auth import logout
from .models import *
from .forms import *


# Rendering views
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

def logout_view(request):
    logout(request)
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
        # If getting a post request...
        if request.method == 'POST':
            # If it's a 'new request' request...
            if request.POST.get('action') == 'Submit':
                title = request.POST['title']
                location = request.POST['location']
                description = request.POST['description']
                new_request = Request()
                new_request.title = title
                new_request.location = location
                new_request.description = description
                new_request.pub_date = timezone.now()
                new_request.user = request.user.email
                new_request.save()
                user = get_user(request)
                user.has_active_request = True
                user.save()
                print("request processed")
                return HttpResponseRedirect('/myRequest')
            # If it's a 'delete request' request...
            elif request.POST.get('action') == 'Delete':
                user = get_user(request)
                email = user.email
                instance = Request.objects.filter(user=email)
                instance.delete()
                user.has_active_request = False
                user.save()
                return HttpResponseRedirect('/myRequest')

        # Otherwise, a GET request. just loading the page
        else:
            requests_list = Request.objects.order_by('-pub_date')[:]
            context = {
                'requests_list': requests_list,
            }
            return render(request, 'app/myRequest.html', context)
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

# Other views (request handlers)
def deleteRequest(request):
    pass