from __future__ import unicode_literals
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

    last_name = forms.CharField(label=u"H\u1ecd")
    first_name = forms.CharField(label=u"T\xean")
    dob = forms.DateField(label=u"Ng\xe0y sinh [dd/mm/yyyy] ",
                          input_formats=['%d/%m/%Y'])
    password1 = forms.CharField(label=u"M\u1eadt Kh\u1ea9u",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Nh\u1eadp l\u1ea1i m\u1eadt kh\u1ea9u",
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
            raise forms.ValidationError(
                u"M\u1eadt kh\u1ea9u nh\u1eadp l\u1ea1i sai!")
        return password2


    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
            raise forms.ValidationError(
                u"username n\xe0y \u0111\xe3 \u0111\u01b0\u1ee3c \u0111\u0103ng k\xfd b\u1edfi t\xe0i kho\u1ea3n kh\xe1c")
        except User.DoesNotExist:
            pass
        return username


    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            try:
                user = User.objects.get(email=email)
                if user is not None:
                    raise ValidationError(
                        u"Email n\xe0y \u0111\xe3 \u0111\u01b0\u1ee3c s\u1eed d\u1ee5ng!!")
            except User.DoesNotExist:
                pass       
        except ValidationError:
            pass
        return email


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
