from django.contrib import admin
from .models import (
    JobTitle,
    Locality,
    HealthProvider,
    PensionFund,
    CompensationFund,
    SavingFund,
    Headquarter,
    Management,
    Campaign,
    Bank,
)


admin.site.register(Bank)
admin.site.register(PensionFund)
admin.site.register(CompensationFund)
admin.site.register(SavingFund)
admin.site.register(Headquarter)
admin.site.register(Locality)


@admin.action(description="Cambiar el estado a activo")
def enable(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description="Cambiar el estado a inactivo")
def disable(modeladmin, request, queryset):
    queryset.update(status=False)


# Register your models here.
@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]


@admin.register(HealthProvider)
class HealthProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]


@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "status")
    search_fields = ("name",)
    list_filter = ("status",)
    list_per_page = 25
    list_max_show_all = 100
    ordering = ("name",)
    actions = [enable, disable]
