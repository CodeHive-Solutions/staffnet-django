from django.contrib import admin

from .models import CustomUser


# ! Remember implement a attempts max limit for login
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active", "is_superuser")
    list_filter = ("is_active", "is_superuser")
    list_per_page = 25
    list_max_show_all = 100
    actions = ["enable", "disable"]

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def enable(self, request, queryset):
        queryset.update(is_active=True)

    enable.short_description = "Enable selected users"

    def disable(self, request, queryset):
        queryset.update(is_active=False)

    disable.short_description = "Disable selected users"
