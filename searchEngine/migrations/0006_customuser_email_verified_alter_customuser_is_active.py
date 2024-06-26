# Generated by Django 5.0.6 on 2024-05-10 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchEngine', '0005_customuser_active_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
