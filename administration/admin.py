from django.contrib import admin
from django.http import HttpRequest

from .models import (
    Bank,
    Campaign,
    CompensationFund,
    Headquarter,
    HealthProvider,
    JobTitle,
    Locality,
    Management,
    PensionFund,
    SavingFund,
)

admin.site.site_header = "Administración de StaffNet"
admin.site.site_title = "StaffNet Admin"


@admin.action(description="Cambiar el estado a activo")
def enable(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description="Cambiar el estado a inactivo")
def disable(modeladmin, request, queryset):
    queryset.update(status=False)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(PensionFund)
class PensionFundAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(CompensationFund)
class CompensationFundAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(SavingFund)
class SavingFundAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Headquarter)
class HeadquarterAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ("name",)

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


# Register your models here.
@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "rank", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(HealthProvider)
class HealthProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]

    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
