from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.htpp import HttpResponse
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


def feed(request):
    if request.user.is_authenticated:
        # handle post request
        if request.method == 'POST':
            # If it's a 'logout' request...
            if request.POST.get('action') == 'Logout':
                logout(request)
                return HttpResponseRedirect('/')
        # handle get request
        else:
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
            # If it's an 'edit request' request...
            elif request.POST.get('action') == 'Edit':
                user = get_user(request)
                request_to_edit = Request.objects.get(user=user.email)
                title = request_to_edit.title
                location = request_to_edit.location
                description = request_to_edit.description
                context = {
                    'title': title,
                    'location': location,
                    'description': description
                }
                return render(request, 'app/requestEditor.html', context)
            # If they've decided to update the request...
            if request.POST.get('action') == 'Update':
                user = get_user(request)
                request_to_edit = Request.objects.get(user=user.email)
                request_to_edit.title = request.POST['title']
                request_to_edit.location = request.POST['location']
                request_to_edit.description = request.POST['description']
                request_to_edit.save()
                context = {
                    'request': request_to_edit,
                }
                return render(request, 'app/myRequest.html', context)
            # If it's a 'logout' request...
            elif request.POST.get('action') == 'Logout':
                logout(request)
                return HttpResponseRedirect('/')

        # Otherwise, a GET request. just loading the page
        else:
            user = get_user(request)
            # If the user has a request, get it and pass it to the view for display
            # be wary of the case where the boolean is true but they don't actually have a request... bug?
            if user.has_active_request:
                my_request = Request.objects.get(user=user.email)
                context = {
                    'request': my_request
                }
                return render(request, 'app/myRequest.html', context)
            # Otherwise, we don't need to pass anything
            else:
                return render(request, 'app/myRequest.html')
    # If not authenticated
    else:
        return HttpResponseRedirect('/')


def profile(request):
    if request.user.is_authenticated:
        # handle post request
        if request.method == 'POST':
            # If it's a 'logout' request...
            if request.POST.get('action') == 'Logout':
                logout(request)
                return HttpResponseRedirect('/')
        # handle get request
        else:
            return render(request, 'app/profile.html')
    else:
        return HttpResponseRedirect('/')


def contacts(request):
    if request.user.is_authenticated:
        # handle post request
        if request.method == 'POST':
            # If it's a 'logout' request...
            if request.POST.get('action') == 'Logout':
                logout(request)
                return HttpResponseRedirect('/')
        # handle get request
        else:
            return render(request, 'app/contacts.html')
    else:
        return HttpResponseRedirect('/')

def messages(request):
    if request.user.is_authenticated:
        return render(request, 'app/messages.html')
    else:
        return HttpResponseRedirect('/')

def offerHelp(request, requestor):
    if request.user.is_authenticated:
        # handle post request
        if request.method == 'POST':
            if request.POST.get('action') == 'Offer Help':
                temp_tutor = get_user(request)
                request_to_edit = Request.objects.get(user=requestor)
                temp_tutor = Tutor(email=get_user(request))
                temp_tutor.save()
                request_to_edit.tutors.add(temp_tutor)
                request_to_edit.save()

                # if (request_to_edit.tutors is not None):
                #     if (request_to_edit.tutors.find(temp_tutor.email) == -1):
                #         request_to_edit.tutors = request_to_edit.tutors + ' ' + temp_tutor.email
                # request_to_edit.save()
                return HttpResponse('<h1> You have offered help to {}</h1>'.format(requestor))
    else:
        return HttpResponseRedirect('/')