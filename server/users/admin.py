from django.contrib import admin
from .models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["username"]


admin.site.unregister(Group)
admin.site.unregister(Token)
