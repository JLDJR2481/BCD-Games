from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from .views import RootView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootView.as_view(), name='home'),
    path('search/', include('searchEngine.urls')),
    path('posts/', include('gamesPosts.urls')),
    path('user/', include('user.urls')),
    path('game/', include('game.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
