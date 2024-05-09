from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login

from searchEngine.models import CustomUser

from django.core.mail import send_mail
import os
import random


class RootView(View):
    def get(self, request):
        return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    fields = "__all__"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, "El inicio de sesión ha fallado. Compruebe los datos introducidos")
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if not self.request.is_active:
            self.request.session["user_id"] = self.request.user.id
            return redirect("verify")

        return response

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = "/"


class UserRegisterView(FormView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("verify")

    def form_valid(self, form):
        user_verification_code = random.randint(100000, 999999)
        user = form.save()
        user.is_active = False
        user.active_code = user_verification_code
        user.save()
        email = user.email

        if user is not None:
            send_mail(
                "Código de verificación BCD-Games",
                f"Te damos la bienvenida a BCD-Games! Utiliza este código para verificar tu registro: {user_verification_code}",
                "bcd.games2001@gmail.com",
                [f"{email}"],
                auth_password=os.environ.get("SMTP_APP_PASS")
            )

            self.request.session["user_id"] = user.id

        else:
            messages.error(
                self.request, "El registro ha fallado. Por favor, inténtalo de nuevo.")
            return render(self.request, "registration/register.html")

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserVerifyView(View):
    def get(self, request):
        return render(request, "registration/verify.html")

    def post(self, request):
        input_code = request.POST.get("verification-code")
        user = CustomUser.objects.get(id=request.session["user_id"])

        active_code = user.active_code

        if user and active_code == int(input_code):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(
                request, "Código de verificación incorrecto. Por favor, inténtalo de nuevo.")
            return render(request, "registration/verify.html")


class UserUpdateView(View):
    def get(self, request):
        return render(request, "users/edit-profile.html")

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES,
                              instance=request.user)
        if form.is_valid():
            form.save()

        else:
            form = UserUpdateForm(instance=request.user)
        return render(request, "users/edit-profile.html", {"form": form})


class ForgotPasswordEmailView(View):
    def get(self, request):
        return render(request, "registration/forgot-password.html")

    def post(self, request):
        user = CustomUser.objects.filter(
            email=request.POST.get("email")).first()

        if user:
            email = user.email
            code = random.randint(100000, 999999)
            user.active_code = code
            user.save()
            send_mail(
                "¿Has olvidado tu contraseña?",
                f"Si has solicitado recuperar tu contraseña, escribe este código de verificación: {code}",
                "bcd.games2001@gmail.com",
                [f"{email}"],
                auth_password=os.environ.get("SMTP_APP_PASS")
            )

            return redirect("verify-forgot-password")
        else:
            messages.error(
                request, "No se ha encontrado ningún usuario con ese correo electrónico. Por favor, inténtalo de nuevo.")
            return render(request, "registration/forgot-password.html")


class VerifyForgotPasswordView(View):
    def get(self, request):
        return render(request, "registration/verify-forgot-password.html")

    def post(self, request):
        user_id = self.request.session["user_id"]

        user = CustomUser.objects.get(id=user_id)
        code = user.active_code

        input_code = request.POST.get("verification-code")

        if user and int(input_code) == code:
            return redirect("reset-password")

        else:
            messages.error(
                request, "Código de verificación incorrecto. Por favor, inténtalo de nuevo.")
            return render(request, "registration/verify-forgot-password.html")


class ResetPasswordView(View):
    def get(self, request):
        return render(request, "registration/reset-password.html")

    def post(self, request):
        user_id = self.request.session["user_id"]
        user = CustomUser.objects.get(id=user_id)

        password = request.POST.get("password")
        confirm_password = request.POST.get("password2")

        if password == confirm_password:
            user.password = password
            user.save()
            return redirect("login")

        else:
            messages.error(
                request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            return render(request, "registration/reset-password.html")


def custom_404(request, exception):
    return render(request, '404.html', status=404)
