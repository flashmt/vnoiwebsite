from avatar.forms import UploadAvatarForm
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.views import _get_avatars, _get_next
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from vnoiusers.forms import UserLoginForm, UserCreateForm, CodeforcesLinkForm, VojLinkForm, FriendSearchForm


def user_login(request, template_name='vnoiusers/user_login.html'):
    form = UserLoginForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main')

    if request.POST:
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if (user is not None) and user.is_active:
                login(request, user)
                messages.success(request, 'Welcome back, %s' % username)
                last_url = request.META.get('HTTP_REFERER')
                if '/user/register' in last_url or '/user/login' in last_url:
                    last_url = reverse('main:index')
                return HttpResponseRedirect(last_url)
            else:
                return render(request, template_name, {'form': form, 'message': 'login fail!'})
        except KeyError:
            return render(request, template_name, {'form': form, 'message': 'login fail!'})
    else:
        return render(request, template_name, {'form': form, 'message': ''})


def user_logout(request):
    logout(request)
    return redirect('main:index')


def user_create(request, template_name='vnoiusers/user_create.html'):
    form = UserCreateForm()
    if request.user.is_authenticated():
        messages.warning(request, 'Invalid request')
        return HttpResponseRedirect('/main')

    if request.POST:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            try:
                username = request.POST['username']
                password = request.POST['password2']
                last_name = request.POST['last_name']
                first_name = request.POST['first_name']
                dob = request.POST['dob']
                email = request.POST['email']
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    last_name=last_name,
                    first_name=first_name,
                    email=email
                )
                return redirect('user:login')
            except KeyError:
                return render(request, template_name,
                              {'form': form, 'message': 'Please fill out all boxes'})
        else:
            return render(request, template_name,
                          {'form': form, 'message': form.errors})
    else:
        return render(request, template_name,
                      {'form': form, 'message': ''})


def user_update(request, user_id):
    pass


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    is_authenticated = False
    is_friend = False
    if request.user.is_authenticated():
        is_authenticated = request.user.username == user.username
        vnoi_user = request.user.profile
        is_friend = True if vnoi_user.friends.filter(id=user_id) else False

    context = {
        'profile_user': user,
        'is_authenticated': is_authenticated,
        'topics': user.created_topics.all(),
        'disable_breadcrumbs': True,
        'is_friend': is_friend,
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


@login_required
def link_codeforces_account(request):
    template_name = 'vnoiusers/link_codeforces.html'
    if request.POST:
        form = CodeforcesLinkForm(request.POST)
        if form.is_valid():
            vnoiuser = request.user.profile
            vnoiuser.codeforces_account = request.POST['username']
            vnoiuser.save()
            return HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': request.user.id}))
        else:
            return render(request, template_name, {
                'form': form,
                'message': form.errors
            })
    else:
        return render(request, template_name, {
            'form': CodeforcesLinkForm()
        })

@login_required
def unlink_codeforces_account(request):
    vnoiuser = request.user.profile
    vnoiuser.codeforces_account = ''
    vnoiuser.save()
    return HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': request.user.id}))


@login_required
def link_voj_account(request):
    template_name = 'vnoiusers/link_voj.html'
    if request.POST:
        form = VojLinkForm(request.POST)
        if form.is_valid():
            vnoiuser = request.user.profile
            vnoiuser.voj_account = request.POST['username']
            vnoiuser.save()
            return HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': request.user.id}))
        else:
            return render(request, template_name, {
                'form': form,
                'message': form.errors
            })
    else:
        return render(request, template_name, {
            'form': VojLinkForm()
        })


@login_required
def unlink_voj_account(request):
    vnoiuser = request.user.profile
    vnoiuser.voj_account = ''
    vnoiuser.save()
    return HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': request.user.id}))


@login_required
def add_friend(request, user_id):
    user_id = int(user_id)

    # If the other user does not exist
    other_user = get_object_or_404(User, pk=user_id)

    redirect_obj = HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': user_id}))

    if user_id == request.user.id:
        # Two users are the same
        messages.warning(request, 'You can not add friend yourself')
        return redirect_obj
    else:
        vnoi_user = request.user.profile
        if vnoi_user.friends.filter(id=user_id):
            # Two users are already friends
            messages.warning(request, 'Already friend')
            return redirect_obj

        vnoi_user.friends.add(other_user.profile)
        messages.success(request, 'Friend successfully added')
        vnoi_user.save()
    return redirect_obj


@login_required
def remove_friend(request, user_id):
    user_id = int(user_id)

    # If the other user does not exist
    other_user = get_object_or_404(User, pk=user_id)

    redirect_obj = HttpResponseRedirect(reverse('user:profile', kwargs={'user_id': user_id}))

    if user_id == request.user.id:
        # Two users are the same
        messages.warning(request, 'You can not add friend yourself')
        return redirect_obj
    else:
        vnoi_user = request.user.profile
        if not vnoi_user.friends.filter(id=user_id):
            # Two users are already friends
            messages.warning(request, 'Not friend')
            return redirect_obj

        vnoi_user.friends.remove(other_user.profile)
        messages.success(request, 'Friend successfully removed')
        vnoi_user.save()
    return redirect_obj


@login_required
def friend_list(request):
    return render(request, 'vnoiusers/friends.html', {
        'friends': request.user.profile.friends.all(),
        'form': FriendSearchForm(),
    })


def index(request):
    return None