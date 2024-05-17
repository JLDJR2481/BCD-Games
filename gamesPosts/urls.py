from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeBlogView.as_view(), name="gamesPosts"),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-details'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:post_id>/comment/', PostCommentView.as_view(), name="post-comment"),
    path("comment/<int:comment_id>/like/",
         CommentLikeView.as_view(), name="comment-like"),
    path("comment/<int:comment_id>/subcomment/",
         SubCommentView.as_view(), name="subcomment"),
    path("comment/edit/<int:comment_id>/",
         EditCommentView.as_view(), name="edit-comment"),
    path("comment/delete/<int:comment_id>/",
         DeleteCommentView.as_view(), name="delete-comment"),

    path('create-post/', CreatePostView.as_view(), name="create-post"),
    path('my-posts/', ListOwnPostView.as_view(), name="my-posts"),
    path('edit-post/<int:post_id>/', UpdateOwnPostView.as_view(), name="edit-post"),
    path('delete-post/<int:post_id>/',
         DeleteOwnPostView.as_view(), name="delete-post"),
    path('search/', search, name="search"),
    path("users-posts/<int:user_id>/",
         IndividualUserPostView.as_view(), name="users-posts"),
]
