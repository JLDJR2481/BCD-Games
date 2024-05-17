from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    visual_content = models.ImageField(upload_to="visual_content/")
    publication_date = models.DateTimeField(auto_now_add=True)
    last_update_date = models.DateTimeField(auto_now=True)
    game = models.ForeignKey("searchEngine.Game", on_delete=models.CASCADE)
    author = models.ForeignKey(
        "user.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.like_set.count()

    def count_comments(self):
        return self.comment_set.count()

    def user_has_liked(self, user):
        return self.like_set.filter(user=user).exists()


class Comment(models.Model):
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey("user.CustomUser",
                             on_delete=models.CASCADE)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE,
                                       null=True, blank=True)

    def get_subcomments(self):
        return Comment.objects.filter(parent_comment=self)

    def count_likes(self):
        return self.like_set.count()

    def count_subcomments(self):
        return self.comment_set.count()

    def user_has_liked_comment(self, user):
        return self.like_set.filter(user=user).exists()


class Like(models.Model):
    user = models.ForeignKey("user.CustomUser",
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    like_date = models.DateTimeField(auto_now_add=True)
