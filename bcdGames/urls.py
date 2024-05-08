from django.contrib import admin
from django.urls import path, include, re_path
from .views import RootView, UserLoginView, UserLogoutView, UserRegisterView, UserUpdateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RootView.as_view(), name='home'),
    path('search/', include('searchEngine.urls')),
    path("posts/", include('gamesPosts.urls')),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("update/", UserUpdateView.as_view(), name="update-profile"),
    path('game/', include('game.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
