from django.contrib import admin

from .models import ResumeEntry


@admin.register(ResumeEntry)
class ResumeEntryAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "date_range", "order")
    list_filter = ("section",)
    list_editable = ("order",)
