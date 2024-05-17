from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Comment, Like
from user.models import CustomUser
from django.views import View
from searchEngine.models import Game
from django.http import JsonResponse

from bcdGames.mixins import EmailVerifiedRequiredMixin


def search(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        consulta = request.GET.get("term")
        games = Game.objects.filter(
            name__startswith=consulta).values_list('name', flat=True)
        resultados = [game for game in games]
        return JsonResponse(resultados, safe=False)
    return JsonResponse({}, safe=False)


class HomeBlogView(ListView):
    model = Post
    paginate_by = 10
    template_name = "posts/home.html"
    ordering = ['-publication_date']


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post-details.html"

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)

        post_last_update_date = post.last_update_date if post.last_update_date != post.publication_date else None

        author = CustomUser.objects.get(id=post.author_id)
        comments = Comment.objects.all()

        parent_comments = comments.filter(post=post, parent_comment__isnull=True).order_by(
            "-comment_date")

        likes = Like.objects.filter(post=post)

        child_comments = comments.filter(
            post=post, parent_comment__isnull=False)

        parent_comments_data = []
        likes_data = []

        child_comments_data = []

        for comment in parent_comments.values():
            user = CustomUser.objects.get(id=comment["user_id"])
            comment_like_count = Comment.objects.get(
                id=comment["id"]).count_likes()
            subcomments_count = Comment.objects.get(
                id=comment["id"]).count_subcomments()

            last_update = comment["update_date"] if comment["update_date"] != comment["comment_date"] else None

            comment_data = {
                "id": comment["id"],
                "user": user,
                "content": comment["content"],
                "comment_date": comment["comment_date"],
                "last_update": last_update,
                "likes_count": comment_like_count,
                "subcomments_count": subcomments_count
            }
            parent_comments_data.append(comment_data)

        for like in likes.values():
            user = CustomUser.objects.get(id=like["user_id"])
            like_data = {
                "user": user
            }
            likes_data.append(like_data)

        for subcomment in child_comments.values():
            user = CustomUser.objects.get(id=subcomment["user_id"])
            parent_comment = Comment.objects.get(
                id=subcomment["parent_comment_id"])
            subcomment_likes = Comment.objects.get(
                id=subcomment["id"]).count_likes()

            last_update = subcomment["update_date"] if subcomment["update_date"] != subcomment["comment_date"] else None

            subcomment_data = {
                "id": subcomment["id"],
                "user": user,
                "content": subcomment["content"],
                "comment_date": subcomment["comment_date"],
                "last_update": last_update,
                "parent_comment": parent_comment,
                "subcomment_likes": subcomment_likes
            }
            child_comments_data.append(subcomment_data)

        user_liked_comments_id = []

        if request.user.is_authenticated:
            user_has_liked = post.user_has_liked(request.user)
            for comment in comments:
                if comment.user_has_liked_comment(request.user):
                    user_liked_comments_id.append(comment.id)
        else:
            user_has_liked = False

        likes_count = post.count_likes()
        comments_count = post.count_comments()

        return render(request, self.template_name, {
            "post": post,
            "post_last_update_date": post_last_update_date,
            "author": author,
            "comments": parent_comments_data,
            "likes": likes_data,
            "user_has_liked": user_has_liked,
            "user_liked_comments_id": user_liked_comments_id,
            "likes_count": likes_count,
            "comments_count": comments_count,
            "subcomments": child_comments_data,
            "game": post.game
        })


class PostLikeView(EmailVerifiedRequiredMixin, View):
    def get(self, request, post_id):
        return redirect('post-details', post_id=post_id)

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


class PostCommentView(EmailVerifiedRequiredMixin, View):
    def get(self, request, post_id):
        return redirect('post-details', post_id=post_id)

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user
        content = request.POST.get("comment")

        comment = Comment(user=user, post=post, content=content)
        comment.save()

        return redirect('post-details', post_id=post_id)


class CommentLikeView(EmailVerifiedRequiredMixin, View):
    def post(self, request, comment_id):

        comment = Comment.objects.get(id=comment_id)
        user = request.user

        if comment.user_has_liked_comment(user):
            like = Like.objects.get(user=user, comment=comment)
            like.delete()
        else:
            like = Like(user=user, comment=comment)
            like.save()

        return redirect('post-details', post_id=comment.post.id)


class SubCommentView(EmailVerifiedRequiredMixin, View):
    def post(self, request, comment_id):
        post = Comment.objects.get(id=comment_id).post

        post_id = post.id

        user = request.user
        content = request.POST.get("comment")
        parent_comment = Comment.objects.get(id=comment_id)

        comment = Comment(user=user, post=post, content=content,
                          parent_comment=parent_comment)
        comment.save()

        return redirect('post-details', post_id=post_id)


class EditCommentView(EmailVerifiedRequiredMixin, View):
    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        return render(request, "posts/edit-comment.html", {"comment": comment})

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.content = request.POST.get("content")
        comment.save()
        return redirect('post-details', post_id=comment.post.id)


class DeleteCommentView(EmailVerifiedRequiredMixin, View):
    def get(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        return render(request, "posts/delete-comment.html", {"comment": comment})

    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post.id
        comment.delete()
        return redirect('post-details', post_id=post_id)


class CreatePostView(EmailVerifiedRequiredMixin, View):
    model = Post
    fields = ["title", "content", "visual_content", "game"]
    template_name = "posts/create-post.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST

        game_name = data.get("game")
        game_post = Game.objects.get(name=game_name)

        title = data.get("title")
        content = data.get("content")
        visual_content = request.FILES.get("visual_content")
        author = request.user

        post = Post(title=title, content=content,
                    visual_content=visual_content, game=game_post, author=author)

        post.save()

        return redirect('gamesPosts')


class ListOwnPostView(EmailVerifiedRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = "posts/my-posts.html"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class UpdateOwnPostView(EmailVerifiedRequiredMixin, View):
    model = Post
    fields = ["title", "content", "visual_content", "game"]
    template_name = "posts/edit-post.html"

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, self.template_name, {"post": post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        data = request.POST

        game_name = data.get("game")
        game_post = Game.objects.get(name=game_name)

        post.title = data.get("title")
        post.content = data.get("content")
        post.visual_content = request.FILES.get("visual_content")
        post.game = game_post

        post.save()

        return redirect('my-posts')


class DeleteOwnPostView(EmailVerifiedRequiredMixin, View):
    model = Post
    template_name = "posts/delete-post.html"

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        return render(request, self.template_name, {"post": post})

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return redirect('my-posts')


class IndividualUserPostView(View):
    model = Post
    template = "posts/individual-user-posts.html"

    def get(self, request, user_id):
        author = CustomUser.objects.get(id=user_id)
        posts = Post.objects.filter(
            author=author).order_by('-publication_date')
        return render(request, self.template, {"posts": posts, "author": author})
