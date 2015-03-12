from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from vnoiusers.forms import UserLoginForm


def user_login(request, template_name='vnoiusers/user_login.html'):
    print 'login request received'
    form = UserLoginForm()
    if request.user.is_authenticated():
        # user already logged in
        return render(request, template_name, {'form': form, 'message': 'You already login!'})

    if request.POST:
        print 'Yes, it is post request'
        try:
            username = request.POST['username']
            password = request.POST['password']
            print 'username = %s, password = %s' % (username, password)
            user = authenticate(username=username, password=password)
            if (user is not None) and user.is_active:
                login(request, user)
                return redirect('main:index')
            else:
                return render(request, template_name, {'form': form, 'message': 'login fail!'})
        except KeyError:
            return render(request, template_name, {'form': form, 'message': 'login fail!'})
    else:
        return render(request, template_name, {'form': form, 'message': ''})


def user_logout(request):
    logout(request)
    return redirect('main:index')


def user_create(request, template=None):
    pass


def user_update(request, user_id):
    pass

def user_profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    is_authenticated = False
    if request.user.is_authenticated():
        is_authenticated = request.user.username == user.username
    context = {'user':user, 'is_authenticated':is_authenticated}
    return render(request, 'vnoiusers/user_profile.html', context)
