from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm, UserRegisterForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login


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
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(self.request, user)
                print("Usuario registrado y autenticado correctamente.")
            else:
                print("La autenticación ha fallado.")
        else:
            print("El registro ha fallado.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Formulario inválido:", form.errors)
        return super().form_invalid(form)


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
