from django.contrib import admin
from .models import CustomUser
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import Post

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for managing AbstractBaseUser in Django Admin.
    """

    model = CustomUser

    # ✅ Define the fields to display in the user list
    list_display = ("email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")

    # ✅ Define the fields shown when viewing/editing a user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    # ✅ Define the fields shown when adding a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")  # Allows assigning permissions in admin

# ✅ Register the custom user model
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post)
