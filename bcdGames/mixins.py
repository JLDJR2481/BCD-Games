from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

# Mixin personalizado para limitar que los usuarios no puedan acceder a ninguna funcionalidad limitada hasta que confirme su correo, además de verificar la autenticación del mismo


class EmailVerifiedRequiredMixin(AccessMixin):

    # Método para comprobar si el usuario está autenticado y su correo ha sido verificado
    def dispatch(self, request, *args, **kwargs):

        # Si el usuario no está autenticado, se le redirige a la vista de login
        if not self.is_user_authenticated(request):
            return redirect("login")

        # Si el usuario está autenticado, pero su correo no ha sido verificado, se le redirige a la vista de verificación
        if not self.is_email_verified(request):
            return redirect("verify")

        # Si el usuario está autenticado y su correo ha sido verificado, se le permite acceder a la vista
        return super().dispatch(request, *args, **kwargs)

    # Método para comprobar si el usuario se ha autenticado
    def is_user_authenticated(self, request):
        return request.user.is_authenticated

    # Método para comprobar si el correo del usuario ha sido verificado
    def is_email_verified(self, request):
        return request.user.email_verified
