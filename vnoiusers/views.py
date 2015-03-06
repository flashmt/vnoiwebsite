from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from vnoiusers.forms import UserLoginForm


def user_login(request, template_name='vnoiusers/user_login.html'):

    form = UserLoginForm()
    if request.user.is_authenticated():
        # user already logged in
        return render(request, template_name, {'form': form, 'message': 'You already login!'})

    if request.POST:
        try:
            username = request.POST['username']
            password = request.POST['password']
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
    try:
        user = User.objects.get(pk = user_id)
        fullname = user.last_name+' '+user.first_name
        context = {'name':fullname, 'email':user.email}
        return render(request, 'vnoiusers/profile.html', context)
    except User.DoesNotExist:
        return HttpResponse("The user does not exist !!!")