from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.contrib.auth import login
from user.models import CustomUser, UserImage
from .forms import UserLoginForm, UserRegisterForm, UserUpdateAvatarForm
import os
import random
import re


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(
            self.request, "El inicio de sesión ha fallado. Compruebe los datos introducidos")
        return response

    def form_valid(self, form):
        if not self.request.user.email_verified:
            return redirect("verify")
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        return next_url if next_url else reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = "/"


class UserRegisterView(FormView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("verify")

    def form_valid(self, form):
        user_verification_code = random.randint(0, 999999)
        user = form.save()
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


class UserVerifyView(View):
    def get(self, request):
        return render(request, "registration/verify.html")

    def post(self, request):
        input_code = request.POST.get("verification-code")
        user = CustomUser.objects.get(id=self.request.session["user_id"])
        active_code = user.active_code

        if user and active_code == int(input_code):
            user.email_verified = True
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
        profile_avatar = request.FILES.get("profile_avatar")
        username = request.POST.get("username")
        email = request.POST.get("email")
        old_password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = CustomUser.objects.get(id=request.user.id)

        if profile_avatar:
            if user.userimage_set.exists():
                user_image = user.userimage_set.first()
                user_image.image.delete()

            else:
                user_image = UserImage(user=user)

            user_image.image = profile_avatar
            user_image.save()
            messages.info(request, "Avatar actualizado correctamente.")

        if username and username != user.username:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(
                    request, "El nombre de usuario ya está en uso. Por favor, elige un nombre de usuario diferente.")
            else:
                user.username = username
                messages.info(
                    request, "Nombre de usuario actualizado correctamente.")

        if email and email != user.email:
            if CustomUser.objects.filter(email=email).exists():
                messages.error(
                    request, "El email ya está en uso. Por favor, elige un email diferente.")
            else:
                user.email = email
                code = random.randint(0, 999999)
                user.active_code = code
                user.email_verified = False
                send_mail(
                    "Código de verificación BCD-Games",
                    f"Utiliza este código para verificar tu nuevo email: {code}",
                    "bcd.games2001@gmail.com",
                    [f"{email}"],
                    auth_password=os.environ.get("SMTP_APP_PASS")
                )
                messages.info(
                    request, "Email actualizado correctamente. Acuérdate de verificar tu nuevo email.")

        if user.check_password(old_password):
            if new_password and user.check_password(old_password) != user.check_password(new_password):
                if len(new_password) < 8:
                    messages.error(
                        request, "La nueva contraseña debe tener al menos 8 caracteres")
                if not re.search(r'[A-Z]', new_password):
                    messages.error(
                        request, "La nueva contraseña debe contener al menos una letra mayúscula")
                if not re.search(r'[a-z]', new_password):
                    messages.error(
                        request, "La nueva contraseña debe contener al menos una letra minúscula")
                if not re.search(r'\d', new_password):
                    messages.error(
                        request, "La nueva contraseña debe contener al menos un número")
                if not re.search(r'[!@#$%^&*()_+]', new_password):
                    messages.error(
                        request, "La nueva contraseña debe contener al menos un caracter especial")
                else:
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        messages.info(
                            request, "Contraseña actualizada correctamente.")
                    else:
                        messages.error(
                            request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

        user.save()
        return render(request, "users/edit-profile.html")


class ForgotPasswordEmailView(View):
    def get(self, request):
        return render(request, "registration/forgot-password.html")

    def post(self, request):
        user = CustomUser.objects.filter(
            email=request.POST.get("email")).first()

        if user:
            email = user.email
            code = random.randint(0, 999999)
            user.active_code = code
            user.save()
            send_mail(
                "¿Has olvidado tu contraseña?",
                f"Si has solicitado recuperar tu contraseña, escribe este código de verificación: {code}",
                "bcd.games2001@gmail.com",
                [f"{email}"],
                auth_password=os.environ.get("SMTP_APP_PASS")
            )
            self.request.session["user_id"] = user.id
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
            user.set_password(password)
            user.save()
            return redirect("login")
        else:
            messages.error(
                request, "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")
            return render(request, "registration/reset-password.html")
