from django.contrib import admin
from .models import Channel
from multimedia.admin import MediaWidgetAdmin

# Register your models here.


@admin.register(Channel)
class ChannelAdmin(MediaWidgetAdmin):
    list_display = (
        "name",
        "owner",
        "total_subs",
    )
    exclude = ("subscribers",)
    search_fields = ["name", "owner__username"]
    list_filter = ["owner"]
    image_fields = [
        "profile_pic",
    ]
