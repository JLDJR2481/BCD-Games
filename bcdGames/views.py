from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .forms import UserLoginForm, UserRegisterForm, UserAvatarForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib import messages


class RootView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    fields = "__all__"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = "/"


class UserRegisterView(View):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    redirect_authenthicated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        return super(UserRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super(UserRegisterView, self).get(*args, **kwargs)
