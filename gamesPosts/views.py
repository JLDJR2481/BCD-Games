from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Like
from searchEngine.models import CustomUser
from django.views import View


class HomeBlogView(ListView):
    model = Post
    paginate_by = 10
    template_name = "blog/home.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-details.html"

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        author = CustomUser.objects.get(id=post.author_id)
        comments = Comment.objects.filter(
            post=post).order_by('-comment_date').values()
        likes = Like.objects.filter(post=post).values()

        comments_data = []
        likes_data = []

        for comment in comments:

            user = CustomUser.objects.get(id=comment["user_id"])
            comment_data = {
                "user": user,
                "content": comment["content"],
                "comment_date": comment["comment_date"]
            }
            comments_data.append(comment_data)

        for like in likes:
            user = CustomUser.objects.get(id=like["user_id"])
            like_data = {
                "user": user
            }
            likes_data.append(like_data)

        user_has_liked = post.user_has_liked(request.user)

        likes_count = post.count_likes()
        comments_count = post.count_comments()

        return render(request, self.template_name, {
            'post': post,
            "author": author,
            "comments": comments_data,
            "likes": likes_data,
            "user_has_liked": user_has_liked,
            "likes_count": likes_count,
            "comments_count": comments_count,

        })


class PostLike(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        if post.user_has_liked(user):
            like = Like.objects.get(user=user, post=post)
            like.delete()
        else:
            like = Like(user=user, post=post)
            like.save()

        return redirect('post-details', post_id=post_id)
