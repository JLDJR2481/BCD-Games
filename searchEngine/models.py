
from django.db import models
from django.contrib.auth.models import AbstractUser

from gamesPosts.models import Post
# Create your models here.


class Game(models.Model):
    game_id = models.IntegerField()
    name = models.CharField(max_length=255, db_index=True)
    translated_description_es = models.TextField()
    metacritic = models.IntegerField(null=True)
    released = models.DateField(null=True)
    background_image = models.URLField(null=True)
    average_rating = models.FloatField()
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
