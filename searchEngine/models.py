
from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    profile_avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.username
