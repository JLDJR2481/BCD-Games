from django import forms
from django.contrib.auth import authenticate
from searchEngine.models import CustomUser
import re

from django.contrib.auth import login


# Users forms
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

            else:
                self.user_cache.backend = "django.contrib.auth.backends.ModelBackend"
                login(self.request, self.user_cache)
        return cleaned_data

    def get_user(self):
        return self.user_cache


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar contraseña", widget=forms.PasswordInput)

    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = {
            'username': 'Usuario',
            'email': 'Email',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "El nombre de usuario ya está en uso. Por favor elige un nombre de usuario diferente.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "El email ya está en uso. Por favor elige un email diferente.")
        return email

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        if password:
            if len(password) < 8:
                raise forms.ValidationError(
                    "La contraseña debe tener al menos 8 caracteres")
            if not re.search(r'[A-Z]', password):
                raise forms.ValidationError(
                    "La contraseña debe contener al menos una letra mayúscula")
            if not re.search(r'[a-z]', password):
                raise forms.ValidationError(
                    "La contraseña debe contener al menos una letra minúscula")
            if not re.search(r'\d', password):
                raise forms.ValidationError(
                    "La contraseña debe contener al menos un número")
            if not re.search(r'[!@#$%^&*()_+]', password):
                raise forms.ValidationError(
                    "La contraseña debe contener al menos un caracter especial")

        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_avatar']
        labels = {
            'username': 'Usuario',
            'profile_avatar': 'Avatar',
        }
