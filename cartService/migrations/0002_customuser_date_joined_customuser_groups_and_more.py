# Generated by Django 4.2.3 on 2023-07-21 12:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("cartService", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="date_joined",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customuser",
            name="groups",
            field=models.ManyToManyField(blank=True, to="auth.group"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="user_permissions",
            field=models.ManyToManyField(blank=True, to="auth.permission"),
        ),
    ]
