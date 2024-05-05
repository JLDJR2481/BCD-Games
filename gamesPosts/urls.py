from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeBlogView.as_view(), name="gamesPosts"),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-details'),
    path('<int:post_id>/like/', PostLike.as_view(), name='post-like'),
]
