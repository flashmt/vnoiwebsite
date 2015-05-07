# -*- coding: utf-8 -*-

import hashlib
import random
from avatar.views import _get_avatars
from django.contrib import messages
from django.contrib.auth import logout, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core import serializers
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_decode, is_safe_url

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url

# Create your views here.
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from post_office import mail
from forum.models import Topic, Post, Vote
from vnoiusers.forms import *
from vnoiusers.models import VnoiUser
from configurations.settings import ROOT_URL, DEBUG


def user_login(request,
               template_name='vnoiusers/user_login.html'):
    form = UserLoginForm()
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('main:index'))

    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Welcome back, %s' % form.cleaned_data['username'])

            if 'next' in request.GET:
                next_url = request.GET['next']
            else:
                next_url = request.META.get('HTTP_REFERER')
            if '/user/register' in next_url or '/user/login' in next_url:
                next_url = reverse('main:index')

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=next_url, host=request.get_host()):
                next_url = resolve_url(settings.LOGIN_REDIRECT_URL)

            return HttpResponseRedirect(next_url)
        else:
            return render(request, template_name, {'form': form, 'message': 'login fail!'})
    else:
        return render(request, template_name, {'form': form, 'message': ''})


@login_required
def user_logout(request):
    logout(request)
    return redirect('main:index')


def user_create(request, template_name='vnoiusers/user_create.html'):
    form = UserCreateForm()
    if request.user.is_authenticated():
        messages.warning(request, 'Invalid request')
        return HttpResponseRedirect(reverse('main:index'))

    if request.POST:
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()  # save user to database if form is valid

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:8]
            activation_key = hashlib.sha1(salt + email).hexdigest()

            # Get user by username
            user = User.objects.get(username=username)
            user.profile.activation_key = activation_key
            user.profile.save()

            # Send email with activation key
            if not DEBUG:
                email_subject = 'Đăng ký tài khoản VNOI'
                email_body = "Hi %s, chào mừng bạn đã đến với VNOI. Để kích hoạt tài khoản, hãy click vào link: %s/user/confirm/%s" % (username, ROOT_URL, activation_key)
                mail.send(email, subject=email_subject, message=email_body, priority="now")
                return HttpResponse('Một email đã được gửi đến tài khoản email mà bạn đăng ký. Hãy kiểm tra hòm thư của bạn và làm theo hướng dẫn để kích hoạt tài khoản.')
            else:
                return HttpResponse('Bạn đã đăng ký thành công. Bạn có thể trở về trang chủ để đăng nhập')
        else:
            return render(request, template_name,
                          {'form': form, 'message': form.errors})
    else:
        return render(request, template_name,
                      {'form': form, 'message': ''})


def register_confirm(request, activation_key):
    # check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse('main:index'))

    # check if there is UserProfile which matches the activation key (if not then display 404)
    vnoiuser = get_object_or_404(VnoiUser, activation_key=activation_key)

    # save user and set him as active and render some template to confirm activation
    user = vnoiuser.user
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('user:login'))


def user_profile(request, username=None):
    user = get_object_or_404(User.objects.select_related("profile", "profile__avatar"), username=username)
    user_id = user.pk

    is_friend = False
    if request.user.is_authenticated():
        authenticated_user = request.user.profile
        is_friend = True if authenticated_user.friends.filter(id=user_id) else False

    topics = Topic.objects.filter(created_by=user).values(
        'id', 'forum', 'title', 'content',
        'created_by', 'created_by__username', 'created_at',
        'post__id', 'post__num_upvotes', 'post__num_downvotes',
        'forum__forum_group__group_type'
    )
    if request.user.is_authenticated():
        post_ids = Post.objects.filter(created_by=user).values('id')
        votes = Vote.objects.filter(post_id__in=post_ids, created_by=request.user).values('post_id', 'type')
    else:
        votes = None

    context = {
        'user': user,
        # We must select forum & forum_group, so that get_absolute_url does not need additional queries
        'topics': topics,
        'disable_breadcrumbs': True,
        'is_friend': is_friend,
        'votes': votes,
    }
    return render(request, 'vnoiusers/user_profile.html', context)


@login_required
def user_upload_avatar(request, extra_context=None,
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
            messages.success(request, "Đổi hình đại diện thành công.")

            # Save avatar into user_profile
            user_profile = request.user.profile
            user_profile.avatar = avatar
            user_profile.save()
            return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
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
            return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))
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
    return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))


@login_required
def link_voj_account(request):
    template_name = 'vnoiusers/link_voj.html'
    if request.POST:
        form = VojLinkForm(request.POST)
        if form.is_valid():
            vnoiuser = request.user.profile
            vnoiuser.voj_account = request.POST['username']
            vnoiuser.save()
            return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))
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
    return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))


@login_required
def add_friend(request, username=None):
    # If the other user does not exist
    other_user = get_object_or_404(User, username=username)
    user_id = other_user.pk

    redirect_obj = HttpResponseRedirect(reverse('user:profile', kwargs={'username': username}))

    if user_id == request.user.id:
        # Two users are the same
        messages.warning(request, 'Bạn không thể kết bạn với chính mình')
        return redirect_obj
    else:
        vnoi_user = request.user.profile
        if vnoi_user.friends.filter(id=user_id):
            # Two users are already friends
            messages.warning(request, 'Already friend')
            return redirect_obj

        vnoi_user.friends.add(other_user.profile)
        print other_user.profile.id
        messages.success(request, 'Kết bạn thành công.')
        vnoi_user.save()
    return redirect_obj


@login_required
def remove_friend(request, username=None):
    # If the other user does not exist
    other_user = get_object_or_404(User, username=username)
    user_id = other_user.pk

    redirect_obj = HttpResponseRedirect(reverse('user:profile', kwargs={'username': username}))

    if user_id == request.user.id:
        # Two users are the same
        messages.warning(request, 'Bạn không thể kết bạn với chính mình')
        return redirect_obj
    else:
        vnoi_user = request.user.profile
        if not vnoi_user.friends.filter(id=user_id):
            # Two users are already friends
            messages.warning(request, 'Not friend')
            return redirect_obj

        vnoi_user.friends.remove(other_user.profile)
        messages.success(request, 'Ngừng kết bạn thành công')
        vnoi_user.save()
    return redirect_obj


@login_required
def friend_list(request):
    return render(request, 'vnoiusers/friends.html', {
        'friends': request.user.profile.friends.all(),
        'form': FriendSearchForm(),
    })


@login_required
def index(request):
    if request.POST:
        return render(request, 'vnoiusers/user_list.html', {
            'users': User.objects.filter(username__startswith=request.POST['user_prefix'])[:20],
            'form': FriendSearchForm(),
        })
    else:
        return render(request, 'vnoiusers/user_list.html', {
            'users': None,
            'form': FriendSearchForm(),
        })


@login_required
def update_profile(request):
    if request.POST:
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile', kwargs={'username': request.user.username}))
        else:
            return render(request, 'vnoiusers/update_profile.html', {
                'form': form,
                'message': form.errors
            })
    return render(request, 'vnoiusers/update_profile.html', {
        'form': UserProfileForm(instance=request.user)
    })

# 4 views for password reset:
# - password_reset sends the mail
# - password_reset_done shows a success message for the above
# - password_reset_confirm checks the link the user clicked and
#   prompts for a new password
# - password_reset_complete shows a success message for the above


@csrf_protect
def password_reset(request,
                   template_name='vnoiusers/password_reset.html',
                   email_template_name='vnoiusers/password_reset_email.html',
                   subject_template_name='vnoiusers/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('user:password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_done(request,
                        template_name='vnoiusers/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='vnoiusers/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('user:password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Nhập mật khẩu mới')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Mật khẩu thay đổi không thành công')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='vnoiusers/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='vnoiusers/password_change.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('user:password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='vnoiusers/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def get_user_from_voj_account(request, voj_accounts):
    voj_accounts = voj_accounts.split(';')
    users = VnoiUser.objects.filter(voj_account__in=voj_accounts)
    return JsonResponse(serializers.serialize('json', users, fields=('voj_account', )), safe=False)
