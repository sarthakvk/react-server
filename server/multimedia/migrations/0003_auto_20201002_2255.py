# Generated by Django 3.1.1 on 2020-10-02 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multimedia', '0002_auto_20201002_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='views',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
