from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeBlogView.as_view(), name="gamesPosts"),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-details'),
    path('<int:post_id>/like/', PostLike.as_view(), name='post-like'),
    path('<int:post_id>/comment/', PostComment.as_view(), name="post-comment"),
    path('create-post/', CreatePost.as_view(), name="create-post"),
    path('my-posts/', ListOwnPost.as_view(), name="my-posts"),
    path('edit-post/<int:post_id>/', UpdateOwnPost.as_view(), name="edit-post"),
    path('delete-post/<int:post_id>/',
         DeleteOwnPost.as_view(), name="delete-post"),
    path('search/', search, name="search"),
]
