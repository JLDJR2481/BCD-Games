from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Comment, Like
from searchEngine.models import CustomUser


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
        comments = Comment.objects.filter(post=post).values()

        comments_data = []

        for comment in comments:

            user = CustomUser.objects.get(id=comment["user_id"])
            comment_data = {
                "user": user,
                "content": comment["content"],
                "comment_date": comment["comment_date"]
            }
            comments_data.append(comment_data)

        return render(request, self.template_name, {'post': post, "author": author, "comments": comments_data})
