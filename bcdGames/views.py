from django.shortcuts import render
from django.views import View


# Vista de la página principal
class RootView(View):
    """
    Maneja la vista de la página principal. Devuelve el template index.html
    """

    def get(self, request):
        return render(request, 'index.html')

# Método que maneja la vista de error 404. Separada de las vistas de la aplicación para personalizar el template de error


def custom_404(request):
    """
    Maneja la vista de error 404. Devuelve el template 404.html
    """
    return render(request, '404.html', status=404)
