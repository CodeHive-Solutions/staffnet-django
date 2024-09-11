from django.contrib import admin
from .models import (
    Department,
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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    # search_fields = ("name", "code")
    # list_filter = ("created_at", "updated_at")


# Register your models here.
admin.site.register(JobTitle)
admin.site.register(Locality)
admin.site.register(HealthProvider)
admin.site.register(PensionFund)
admin.site.register(CompensationFund)
admin.site.register(SavingFund)
admin.site.register(Headquarter)
admin.site.register(Management)
admin.site.register(Campaign)
admin.site.register(Bank)
