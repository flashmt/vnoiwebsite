from django import forms
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

    dob = forms.DateTimeField()
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

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
            raise forms.ValidationError("Confirm Password don't match!")
        return password2

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
