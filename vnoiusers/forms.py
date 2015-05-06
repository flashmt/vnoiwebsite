# -*- coding: utf-8 -*-
from collections import OrderedDict

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from configurations.settings import DEBUG
from externaljudges.crawler.codeforces import verify_codeforces_account
from externaljudges.crawler.voj import verify_voj_account
from vnoiusers.models import VnoiUser

import os
from avatar.models import Avatar
from django.template.defaultfilters import filesizeformat
from avatar.conf import settings
from django.utils.translation import ugettext_lazy as _


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.user_cache = None

    class Meta:
        model = User
        fields = ('username',)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u"Tên hoặc mật khẩu nhập không đúng")
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in
            + allow login by active users, and reject login by inactive users.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(u"Người dùng này chưa được kích hoạt")

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class UserCreateForm(forms.ModelForm):
    last_name = forms.CharField(label=u"Họ", max_length=30)
    first_name = forms.CharField(label=u"Tên", max_length=30)
    dob = forms.DateField(label=u"Ngày sinh",
                          input_formats=['%Y-%m-%d'],
                          widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))
    password1 = forms.CharField(label=u"Mật khẩu",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=u"Nhập lại mật khẩu",
                                widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['username'].widget.attrs['placeholder'] = u'VD: code_sieu_nhanh, I_am_cool...'
        self.fields['email'].widget.attrs['placeholder'] = u'Link kích hoạt tài khoản sẽ được gửi đến email này'
        self.fields['last_name'].widget.attrs['placeholder'] = u'VD: Nguyễn, Trần...'
        self.fields['first_name'].widget.attrs['placeholder'] = u'VD: Bình An, Hùng Cường...'
        self.fields['password1'].widget.attrs['placeholder'] = u'Một mật khẩu tốt thường có cả chữ cái in hoa, in thường và chữ số'

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check if 2 passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u"Mật khẩu nhập lại không khớp")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError(u"Tài khoản này đã được đăng ký")
        except User.DoesNotExist:
            pass
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        validate_email(email)
        try:
            user = User.objects.filter(email=email)
            if user:
                raise ValidationError(u"Email này đã được đăng ký!")
        except User.DoesNotExist:
            pass
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            # Activate account or not? Use settings DEBUG
            if DEBUG:
                user.is_active = True  # not active until user opens activation confirmation link
            else:
                user.is_active = False
            user.save()             # Note: post_save signal automatically create a new user profile
            # Update user_profile
            user.profile.dob = self.cleaned_data['dob']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.profile.save()
            user.save()
        return user


class CodeforcesLinkForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label='Tài khoản Codeforces',
        widget=forms.TextInput(attrs={'placeholder': u'Tài khoản codeforces.com', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': u'Mật khẩu codeforces.com', 'autocomplete': 'off'}),
        label='Mật khẩu',
        max_length=30
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        other_profile = VnoiUser.objects.filter(codeforces_account=username)
        if other_profile:
            raise forms.ValidationError('Tài khoản Codeforces này đã được kết nối với tài khoản khác')

        verify_result = verify_codeforces_account(username, password)
        if not verify_result['success']:
            raise forms.ValidationError(verify_result['message'])

        return self.cleaned_data


class VojLinkForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        label='Tài khoản VOJ',
        widget=forms.TextInput(attrs={'placeholder': u'Tài khoản vn.spoj.com', 'autocomplete': 'off'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': u'Mật khẩu vn.spoj.com', 'autocomplete': 'off'}),
        label='Mật khẩu',
        max_length=30
    )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        other_profile = VnoiUser.objects.filter(voj_account=username)
        if other_profile:
            raise forms.ValidationError('Tài khoản VOJ này đã được kết nối với tài khoản khác')

        verify_result = verify_voj_account(username, password)
        if not verify_result['success']:
            raise forms.ValidationError(verify_result['message'])

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(label=u"Ngày sinh",
                          input_formats=['%Y-%m-%d'],
                          widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].label = u'Họ'
        self.fields['first_name'].label = u'Tên'

    class Meta:
        model = User
        fields = ('last_name', 'first_name', )

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.dob = self.cleaned_data['dob']

        if commit:
            user.save()
            user.profile.save()
        return user


class FriendSearchForm(forms.Form):
    user_prefix = forms.CharField(max_length=10, min_length=4, label="Tên tài khoản")


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        email = self.cleaned_data["email"]
        active_users = User.objects.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old password
    """
    error_messages = {
        'password_mismatch': "2 mật khẩu không khớp",
    }
    new_password1 = forms.CharField(label="Mật khẩu mới", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Nhập lại mật khẩu mới", widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        # self.fields['password'].label = 'Mật khẩu cũ'

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': "Mật khẩu cũ không đúng",
    })
    old_password = forms.CharField(label="Mật khẩu cũ",
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)


class UploadAvatarForm(forms.Form):

    avatar = forms.ImageField(label=_("avatar"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UploadAvatarForm, self).__init__(*args, **kwargs)

    def clean_avatar(self):
        data = self.cleaned_data['avatar']

        if settings.AVATAR_ALLOWED_FILE_EXTS:
            root, ext = os.path.splitext(data.name.lower())
            if ext not in settings.AVATAR_ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(settings.AVATAR_ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. "
                          "Authorized extensions are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                             'valid_exts_list': valid_exts})

        if data.size > settings.AVATAR_MAX_SIZE:
            error = _("Your file is too big (%(size)s), "
                      "the maximum allowed size is %(max_valid_size)s")
            raise forms.ValidationError(error % {
                'size': filesizeformat(data.size),
                'max_valid_size': filesizeformat(settings.AVATAR_MAX_SIZE)
            })

        count = Avatar.objects.filter(user=self.user).count()
        if (settings.AVATAR_MAX_AVATARS_PER_USER > 1) and (count >= settings.AVATAR_MAX_AVATARS_PER_USER):
            error = _("You already have %(nb_avatars)d avatars, "
                      "and the maximum allowed is %(nb_max_avatars)d.")
            raise forms.ValidationError(error % {
                'nb_avatars': count,
                'nb_max_avatars': settings.AVATAR_MAX_AVATARS_PER_USER,
            })
        return
