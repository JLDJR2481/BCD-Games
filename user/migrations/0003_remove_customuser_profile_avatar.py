# Generated by Django 5.0.6 on 2024-05-15 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile_avatar',
        ),
    ]
