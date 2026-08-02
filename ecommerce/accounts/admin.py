
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_staff_member', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('E-commerce info', {'fields': ('phone_number', 'is_staff_member')}),
    )