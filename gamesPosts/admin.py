from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')


class CommentModelAdmin(admin.ModelAdmin):
    list_display = ('content', 'comment_date', 'post', 'user')


class LikeModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'like_date')


admin.site.register(Post, PostModelAdmin)
admin.site.register(Comment, CommentModelAdmin)
admin.site.register(Like, LikeModelAdmin)
