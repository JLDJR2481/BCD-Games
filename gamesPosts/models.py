from django.db import models
from searchEngine.models import Game, CustomUser


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    visual_content = models.ImageField(upload_to="visual_content/")
    publication_date = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.like_set.count()

    def count_comments(self):
        return self.comments_set.count()

    def user_has_liked(self, user):
        return self.like_set.filter(user=user).exists()


class Comment(models.Model):
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)
