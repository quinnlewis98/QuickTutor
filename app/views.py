from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth import get_user
from django.contrib.auth import logout
from .models import *
from .forms import *
from django.contrib import messages

# Rendering views
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    else:
        return render(request, 'app/index.html')


# The old redirect page -- was giving some form submission errors. Deemed unnecessary
# def redirect(request):
#     if request.user.is_authenticated:
#         return render(request, 'app/redirect.html')
#     else:
#         return HttpResponseRedirect('/')


def feed(request):
    if request.user.is_authenticated:
        # handle post request
        if request.method == 'POST':
            # If it's an 'offer help' request...
            if request.POST.get('action') == 'Offer Help':
                tutor = get_user(request)
                tutee = request.POST.get('tutee')
                request_to_edit = Request.objects.get(user=tutee)
                request_to_edit.tutors.add(tutor)
                request_to_edit.save()
                return HttpResponseRedirect('/feed')
            # If it's a 'revoke offer' request...
            elif request.POST.get('action') == 'Revoke Offer':
                tutor = get_user(request)
                tutee = request.POST.get('tutee')
                request_to_edit = Request.objects.get(user=tutee)
                request_to_edit.tutors.remove(tutor)
                request_to_edit.save()
                return HttpResponseRedirect('/feed')
            # If it's a 'view profile' request
            elif request.POST.get('action') == 'View Profile':
                tutee = request.POST.get('tutee')
                tutee_user = User.objects.get(email=tutee)
                context = {
                    'tutorORtutee': tutee_user,
                }
                return render(request, 'app/profile.html', context)
            # If it's a 'logout' request...
            elif request.POST.get('action') == 'Logout':
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
                # Make sure they don't have an active request
                user = get_user(request)
                if user.has_active_request:
                    return HttpResponseRedirect('/myRequest')

                # If they don't, go ahead and create the request with their entered data
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

                # Set their boolean flag
                user.has_active_request = True
                user.save()

                # Use redirect to refresh the page
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
            # If they've decided to update the request... (saving the edited changes)
            elif request.POST.get('action') == 'Update':
                user = get_user(request)
                request_to_edit = Request.objects.get(user=user.email)
                request_to_edit.title = request.POST['title']
                request_to_edit.location = request.POST['location']
                request_to_edit.description = request.POST['description']
                request_to_edit.save()
                context = {
                    'request': request_to_edit,
                }
                return HttpResponseRedirect('/myRequest/')
            # If they're trying to view a tutor's profile...
            elif request.POST.get('action') == 'View Profile':
                tutor = request.POST.get('tutor')
                tutor_user = User.objects.get(email=tutor)
                context = {
                    'tutorORtutee': tutor_user,
                }
                return render(request, 'app/profile.html', context)
            # If they're trying to accept a request...
            elif request.POST.get('action') == 'Accept and Delete':
                # Delete the request, and set boolean
                user = get_user(request)
                request_to_edit = Request.objects.get(user=user.email)
                request_to_edit.delete()
                user.has_active_request = False
                user.save()

                # It should automatically add the tutor as a contact and direct you to a message with them!
                return HttpResponseRedirect('/contacts/')
            # If it's a 'logout' request...
            elif request.POST.get('action') == 'Logout':
                logout(request)
                return HttpResponseRedirect('/')

        # Otherwise, a GET request. just loading the page
        else:
            user = get_user(request)
            # If the user has a request, get it and pass it to the view for display
            if user.has_active_request:
                try:
                    my_request = Request.objects.get(user=user.email)
                except:
                    my_request = None
                context = {
                    'request': my_request
                }
                return render(request, 'app/myRequest.html', context)
            # Otherwise, we don't need to pass anything (no request available -- shows request creation form)
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
            else: 
                u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

                if u_form.is_valid():
                    u_form.save()
                    # messages.success(request, f'Your account has been updated!')
                    return redirect('profile')
        # handle get request
        else:
            u_form = UserUpdateForm(instance=request.user)
        context = {
            'user': get_user(request),
            'u_form': u_form
            }
        return render(request, 'app/profile.html', context)
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