from avatar.forms import UploadAvatarForm
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.views import add, _get_avatars, _get_next
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

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
    user = get_object_or_404(User, pk=user_id)
    is_authenticated = False
    if request.user.is_authenticated():
        is_authenticated = request.user.username == user.username
    context = {
        'profile_user': user,
        'is_authenticated': is_authenticated,
        'topics': user.created_topics.all()
    }
    return render(request, 'vnoiusers/user_profile.html', context)


@login_required
def user_upload_avatar(request, extra_context=None, next_override=None,
                       upload_form=UploadAvatarForm, *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user=request.user)
    if request.method == "POST" and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name, image_file)
            avatar.save()
            messages.success(request, _("Successfully uploaded a new avatar."))
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
            return redirect(next_override or _get_next(request))
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override or _get_next(request),
    }
    context.update(extra_context)
    return render(request, 'vnoiusers/user_upload_avatar.html', context)
