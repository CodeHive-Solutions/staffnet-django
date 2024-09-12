from django.contrib import admin
from django.utils.html import format_html
from .models import Employee


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "identification",
        "first_name",
        "last_name",
        "campaign",
        "job_title",
    )
    # show all fields
    # list_display = [field.name for field in Employee._meta.fields]
    readonly_fields = (
        "photo_thumbnail",
        "legacy_appointment_date",
        "legacy_health_provider",
    )

    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 300px;" />', obj.photo.url)
        return "No hay foto"

    photo_thumbnail.short_description = "Previsualización de la foto"

    search_fields = ("first_name", "last_name", "email")
    list_filter = ("job_title",)
    list_per_page = 20
    list_max_show_all = 100
    ordering = ("first_name", "last_name")
    fieldsets = (
        (
            "Información Personal",
            {
                "fields": (
                    ("photo_thumbnail", "photo"),
                    ("document_type", "identification"),
                    ("expedition_place", "expedition_date"),
                    ("first_name", "last_name"),
                    ("email", "corporate_email"),
                    ("birth_date", "gender"),
                    ("civil_status", "sons"),
                    ("responsible_persons", "stratum"),
                    ("fixed_phone", "cell_phone"),
                    ("emergency_contact", "emergency_relationship", "emergency_phone"),
                    "rh",
                )
            },
        ),
        (
            "Dirección",
            {"fields": (("locality", "address", "neighborhood"),)},
        ),
        (
            "Información educativa",
            {"fields": (("education_level", "title", "ongoing_studies"),)},
        ),
        (
            "Información Laboral",
            {
                "fields": (
                    ("affiliation_date", "health_provider", "legacy_health_provider"),
                    ("pension_fund", "compensation_fund", "saving_fund"),
                    ("payroll_account", "bank"),
                    (
                        "headquarter",
                        "management",
                        "campaign",
                    ),
                    "appointment_date",
                    "legacy_appointment_date",
                    "business_area",
                    "job_title",
                    "contract_type",
                    "entry_date",
                    ("salary", "transportation_allowance"),
                    ("remote_work_application_date", "remote_work"),
                    ("shirt_size", "pant_size", "shoe_size"),
                )
            },
        ),
        (
            "Acciones Disciplinarias",
            {
                "fields": (
                    (
                        "memo_1",
                        "memo_2",
                        "memo_3",
                    )
                )
            },
        ),
    )
