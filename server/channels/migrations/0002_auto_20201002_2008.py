# Generated by Django 3.1.1 on 2020-10-02 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("channels", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="channel",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True,
                related_name="channel_subscribed",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
