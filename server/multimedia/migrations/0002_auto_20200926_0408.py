# Generated by Django 3.1.1 on 2020-09-26 04:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("multimedia", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="likes",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="reply",
            field=models.ManyToManyField(
                blank=True, related_name="_comments_reply_+", to="multimedia.Comments"
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]