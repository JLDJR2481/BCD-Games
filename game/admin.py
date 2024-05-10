from django.contrib import admin

from .models import GameScore


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date')


admin.site.register(GameScore, ScoreAdmin)
