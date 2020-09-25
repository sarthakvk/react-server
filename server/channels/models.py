from django.db import models
from users.models import User

# Create your models here.


class Channel(models.Model):
    """
    model for managing channels
    """

    name = models.CharField(max_length=20, null=False, blank=False)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="channels/profile")
    about = models.TextField(null=True, blank=True)
