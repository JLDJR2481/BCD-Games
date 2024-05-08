from django.contrib import admin

from .models import GameScores


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date')


admin.site.register(GameScores, ScoreAdmin)
