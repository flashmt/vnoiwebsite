# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class UserLoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = User
        fields = ('username',)


class UserCreateForm(forms.ModelForm):

    last_name = forms.CharField(label=u"Họ")
    first_name = forms.CharField(label=u"Tên")
    dob = forms.DateField(label=u"Ngày sinh",
                          input_formats=['%d/%m/%Y'],
                          widget=forms.TextInput(attrs={'placeholder': 'dd/mm/yyyy'}))
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
            user.save()
        return user
