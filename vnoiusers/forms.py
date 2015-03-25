# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from externaljudges.crawler.codeforces import verify_codeforces_account
from externaljudges.crawler.voj import verify_voj_account
from vnoiusers.models import VnoiUser


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ('username',)


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
            user.is_active = False  # not active until user opens activation confirmation link
            user.save()
            # Update user_profile
            user.profile.dob = self.cleaned_data['dob']
            user.profile.save()
        return user


class CodeforcesLinkForm(forms.Form):
    username = forms.CharField(max_length=30, label='Tài khoản Codeforces')
    password = forms.CharField(widget=forms.PasswordInput, label='Mật khẩu', max_length=30)

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
    username = forms.CharField(max_length=30, label='Tài khoản VOJ')
    password = forms.CharField(widget=forms.PasswordInput, label='Mật khẩu', max_length=30)

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


class UserProfileForm(forms.Form):
    last_name = forms.CharField(label=u"Họ", max_length=30)
    first_name = forms.CharField(label=u"Tên", max_length=30)
    dob = forms.DateField(label=u"Ngày sinh",
                          input_formats=['%Y-%m-%d'],
                          widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd'}))

    def clean(self):
        pass


class FriendSearchForm(forms.Form):
    user_prefix = forms.CharField(max_length=10, min_length=4, label="Tên tài khoản")
