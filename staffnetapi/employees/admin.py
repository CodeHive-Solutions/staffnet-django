from django.contrib import admin
from .models import Employee


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "job_title")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("job_title",)
    list_per_page = 10
    list_max_show_all = 100
    ordering = ("first_name", "last_name")
    fieldsets = (
        (
            "Información Personal",
            {
                "fields": (
                    ("document_type", "identification"),
                    ("expedition_place", "expedition_date"),
                    ("first_name", "last_name"),
                    ("email", "corporate_email"),
                    ("birth_date", "gender"),
                    ("civil_status", "sons"),
                    ("responsible_persons", "stratum"),
                    ("fixed_phone", "cell_phone"),
                    ("emergency_contact", "emergency_phone"),
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
                    ("affiliation_date", "health_provider", "pension_fund"),
                    ("compensation_fund", "saving_fund"),
                    ("payroll_account", "bank"),
                    (
                        "headquarter",
                        "management",
                        "campaign",
                    ),
                    "appointment_date",
                    "business_area",
                    "job_title",
                    "contract_type",
                    "entry_date",
                    ("salary", "transportation_allowance"),
                    ("remote_work", "remote_work_application_date"),
                    ("shirt_size", "pant_size", "shoe_size"),
                )
            },
        ),
    )
