# Generated by Django 5.0.6 on 2024-05-17 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamesPosts', '0011_alter_comment_udpate_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='udpate_date',
            new_name='update_date',
        ),
    ]
