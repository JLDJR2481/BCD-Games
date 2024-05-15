from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    active_code = models.IntegerField(null=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
