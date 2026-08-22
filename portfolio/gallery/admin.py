from django.contrib import admin
from django.utils.html import format_html

from .models import Artwork


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = ("title", "code_name", "category", "year", "views", "created_at", "thumb")
    list_filter = ("category", "year")
    search_fields = ("title", "code_name", "category")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("views",)

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;" />', obj.image.url
            )
        return "—"

    thumb.short_description = "Preview"
