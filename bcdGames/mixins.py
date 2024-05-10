from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class EmailVerifiedRequiredMixin(AccessMixin):

    # Mixin personalizado para limitar que los usuarios no puedan acceder a ninguna funcinalidad hasta que confirme su correo

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if not request.user.email_verified:
            return redirect("verify")

        return super().dispatch(request, *args, **kwargs)
