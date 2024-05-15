from django.shortcuts import render
from django.views import View


class RootView(View):
    def get(self, request):
        return render(request, 'index.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
