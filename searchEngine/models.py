
from django.db import models
from django.contrib.auth.models import AbstractUser

from gamesPosts.models import Post
# Create your models here.


class Game(models.Model):
    game_id = models.IntegerField()
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    translated_description_es = models.TextField()
    metacritic = models.IntegerField(null=True)
    released = models.DateField(null=True)
    updated = models.DateField(null=True)
    background_image = models.URLField(null=True)
    website = models.URLField(null=True)
    average_rating = models.FloatField()
    ratings = models.JSONField()
    platforms = models.JSONField()
    stores = models.JSONField()
    genres = models.JSONField()
    tags = models.JSONField()
    developers = models.JSONField(null=True)
    publishers = models.JSONField()
    esbr_ratings = models.JSONField()
    search_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_post_count(self):
        return Post.objects.filter(game=self).count()


class CustomUser(AbstractUser):
    profile_avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    active_code = models.IntegerField(null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
