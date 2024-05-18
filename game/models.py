from django.db import models
from user.models import CustomUser


class GameScore(models.Model):
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
