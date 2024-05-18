from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserUpdateView,
    UserVerifyView,
    ForgotPasswordEmailView,
    VerifyForgotPasswordView,
    ResetPasswordView,
    SocialView
)


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify/', UserVerifyView.as_view(), name='verify'),
    path('forgot-password/', ForgotPasswordEmailView.as_view(),
         name='forgot-password'),
    path('verify-forgot-password/', VerifyForgotPasswordView.as_view(),
         name='verify-forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('update/', UserUpdateView.as_view(), name='update-profile'),
    path('social/<str:username>/', SocialView.as_view(), name='social'),
]
