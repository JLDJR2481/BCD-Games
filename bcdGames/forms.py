from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(label="Username", max_length=18)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Login fallido")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Usuario no activo")
        return cleaned_data

    def get_user(self):
        return self.user_cache


class UserRegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserRegisterForm, self).__init__(*args, **kwargs)
    first_name = forms.CharField(label="First Name", max_length=30)
    email = forms.EmailField(label="Email")
    username = forms.CharField(label="Username", max_length=18)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)


class UserAvatarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserAvatarForm, self).__init__(*args, **kwargs)
    profile_avatar = forms.ImageField(label="Profile Avatar")
