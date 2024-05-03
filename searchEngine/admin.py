from django.contrib import admin
from .models import CustomUser


class CustomModelUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_avatar')


admin.site.register(CustomUser, CustomModelUserAdmin)
