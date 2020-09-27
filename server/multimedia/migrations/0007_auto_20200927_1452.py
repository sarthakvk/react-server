# Generated by Django 3.1.1 on 2020-09-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("multimedia", "0006_auto_20200927_1436"),
    ]

    operations = [
        migrations.RenameField(
            model_name="audio",
            old_name="media_url",
            new_name="content",
        ),
        migrations.RenameField(
            model_name="picture",
            old_name="media_url",
            new_name="content",
        ),
        migrations.RenameField(
            model_name="video",
            old_name="media_url",
            new_name="content",
        ),
        migrations.RemoveField(
            model_name="article",
            name="media_url",
        ),
        migrations.AddField(
            model_name="article",
            name="body",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="content",
            field=models.FileField(
                blank=True, null=True, upload_to="multimedia/article"
            ),
        ),
    ]
