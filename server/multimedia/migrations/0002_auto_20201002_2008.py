# Generated by Django 3.1.1 on 2020-10-02 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("multimedia", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("channels", "0002_auto_20201002_2008"),
    ]

    operations = [
        migrations.AddField(
            model_name="views",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="channel",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="video",
                to="channels.channel",
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="comments",
            field=models.ManyToManyField(
                related_name="video", to="multimedia.Comments"
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="video", to="multimedia.Likes"
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="video", to="multimedia.Tags"
            ),
        ),
        migrations.AddField(
            model_name="video",
            name="views",
            field=models.ManyToManyField(
                blank=True, related_name="video", to="multimedia.Views"
            ),
        ),
        migrations.AddField(
            model_name="savedvideo",
            name="saved_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.savedmedia"
            ),
        ),
        migrations.AddField(
            model_name="savedvideo",
            name="video",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.video"
            ),
        ),
        migrations.AddField(
            model_name="savedpicture",
            name="picture",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.picture"
            ),
        ),
        migrations.AddField(
            model_name="savedpicture",
            name="saved_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.savedmedia"
            ),
        ),
        migrations.AddField(
            model_name="savedmedia",
            name="article",
            field=models.ManyToManyField(
                blank=True,
                related_name="saved_articles",
                through="multimedia.SavedArticle",
                to="multimedia.Article",
            ),
        ),
        migrations.AddField(
            model_name="savedmedia",
            name="audio",
            field=models.ManyToManyField(
                blank=True,
                related_name="saved_audios",
                through="multimedia.SavedAudio",
                to="multimedia.Audio",
            ),
        ),
        migrations.AddField(
            model_name="savedmedia",
            name="picture",
            field=models.ManyToManyField(
                blank=True,
                related_name="saved_pictures",
                through="multimedia.SavedPicture",
                to="multimedia.Picture",
            ),
        ),
        migrations.AddField(
            model_name="savedmedia",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="savedmedia",
            name="video",
            field=models.ManyToManyField(
                blank=True,
                related_name="saved_videos",
                through="multimedia.SavedVideo",
                to="multimedia.Video",
            ),
        ),
        migrations.AddField(
            model_name="savedaudio",
            name="audio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.audio"
            ),
        ),
        migrations.AddField(
            model_name="savedaudio",
            name="saved_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.savedmedia"
            ),
        ),
        migrations.AddField(
            model_name="savedarticle",
            name="article",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.article"
            ),
        ),
        migrations.AddField(
            model_name="savedarticle",
            name="saved_to",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="multimedia.savedmedia"
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="channel",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="picture",
                to="channels.channel",
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="comments",
            field=models.ManyToManyField(
                related_name="picture", to="multimedia.Comments"
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="picture", to="multimedia.Likes"
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="picture", to="multimedia.Tags"
            ),
        ),
        migrations.AddField(
            model_name="picture",
            name="views",
            field=models.ManyToManyField(
                blank=True, related_name="picture", to="multimedia.Views"
            ),
        ),
        migrations.AddField(
            model_name="likes",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="comments",
            name="reply_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="replies",
                to="multimedia.comments",
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
        migrations.AddField(
            model_name="audio",
            name="channel",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="audio",
                to="channels.channel",
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="comments",
            field=models.ManyToManyField(
                related_name="audio", to="multimedia.Comments"
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="audio", to="multimedia.Likes"
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="audio", to="multimedia.Tags"
            ),
        ),
        migrations.AddField(
            model_name="audio",
            name="views",
            field=models.ManyToManyField(
                blank=True, related_name="audio", to="multimedia.Views"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="channel",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="article",
                to="channels.channel",
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="comments",
            field=models.ManyToManyField(
                related_name="article", to="multimedia.Comments"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="likes",
            field=models.ManyToManyField(
                blank=True, related_name="article", to="multimedia.Likes"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="article", to="multimedia.Tags"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="views",
            field=models.ManyToManyField(
                blank=True, related_name="article", to="multimedia.Views"
            ),
        ),
    ]
