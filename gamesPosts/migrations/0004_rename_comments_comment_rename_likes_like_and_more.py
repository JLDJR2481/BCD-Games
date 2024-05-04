# Generated by Django 5.0.4 on 2024-05-04 10:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamesPosts', '0003_rename_user_posts_author'),
        ('searchEngine', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
