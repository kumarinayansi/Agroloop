from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'location', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('AgriFoodHub Profile', {'fields': ('role', 'phone', 'location', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('AgriFoodHub Profile', {'fields': ('role', 'phone', 'location')}),
    )
    search_fields = ['username', 'email', 'phone', 'location']
