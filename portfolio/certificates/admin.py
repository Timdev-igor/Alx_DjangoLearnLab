from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "order")
    list_editable = ("order",)
    search_fields = ("title", "issuer")
