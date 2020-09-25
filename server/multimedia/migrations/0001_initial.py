# Generated by Django 3.1.1 on 2020-09-25 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("channels", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UpdateTiming",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Comments",
            fields=[
                (
                    "updatetiming_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.updatetiming",
                    ),
                ),
                (
                    "reply",
                    models.ManyToManyField(
                        blank=True,
                        related_name="_comments_reply_+",
                        to="multimedia.Comments",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("multimedia.updatetiming",),
        ),
        migrations.CreateModel(
            name="Likes",
            fields=[
                (
                    "updatetiming_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.updatetiming",
                    ),
                ),
                ("val", models.BooleanField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("multimedia.updatetiming",),
        ),
        migrations.CreateModel(
            name="Media",
            fields=[
                (
                    "updatetiming_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.updatetiming",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("Description", models.TextField(blank=True, null=True)),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="multimedia/thumbnail"
                    ),
                ),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="channels.channel",
                    ),
                ),
                (
                    "comments",
                    models.ManyToManyField(
                        related_name="media", to="multimedia.Comments"
                    ),
                ),
                (
                    "likes",
                    models.ManyToManyField(related_name="media", to="multimedia.Likes"),
                ),
            ],
            bases=("multimedia.updatetiming",),
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.media",
                    ),
                ),
                (
                    "image",
                    models.FileField(
                        blank=True, null=True, upload_to="multimedia/article"
                    ),
                ),
                ("content", models.TextField(blank=True)),
            ],
            bases=("multimedia.media",),
        ),
        migrations.CreateModel(
            name="Audio",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.media",
                    ),
                ),
                ("link", models.FileField(upload_to="multimedia/audios")),
            ],
            bases=("multimedia.media",),
        ),
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.media",
                    ),
                ),
                ("link", models.FileField(blank=True, upload_to="multimedia/pictures")),
            ],
            bases=("multimedia.media",),
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "media_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="multimedia.media",
                    ),
                ),
                ("link", models.FileField(upload_to="multimedia/videos")),
            ],
            bases=("multimedia.media",),
        ),
    ]
