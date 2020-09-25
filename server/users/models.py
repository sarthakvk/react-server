from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.


class CustomUserManager(UserManager):
    """
    UserManager
    """

    pass


class User(AbstractUser):
    """
    User model for maintaining users
    """

    # Deleting some fields from default AbstractUser model
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(unique=True, max_length=30, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    saved = models.ManyToManyField("multimedia.Media", related_name="saved_by")
    objects = CustomUserManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
