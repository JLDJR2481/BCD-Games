# Generated by Django 5.0.4 on 2024-05-04 10:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamesPosts', '0001_initial'),
        ('searchEngine', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Like',
            new_name='Likes',
        ),
        migrations.RenameModel(
            old_name='Post',
            new_name='Posts',
        ),
    ]
