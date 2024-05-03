from django import forms
from django.contrib.auth import authenticate
from searchEngine.models import CustomUser


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


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        labels = {
            'username': 'Usuario',
            'email': 'Email',
        }

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

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
