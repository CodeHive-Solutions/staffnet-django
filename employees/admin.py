from django.contrib import admin
from django.utils.html import format_html

from .models import Employee


@admin.display(description="Nombre completo")
def get_full_name(obj):
    return obj.get_full_name()


# Register your models here.
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # def photo_thumbnail(self, obj):
    #     if obj.photo:
    #         return format_html('<img src="{}" style="height: 300px;" />', obj.photo.url)
    #     return "No hay foto"

    # photo_thumbnail.short_description = "Previsualización de la foto"

    # fieldsets = (("Información Personal", {"fields": ("personal_info__first_name", "personal_info__last_name")}),)
    search_fields = (
        "personal_info__first_name",
        "personal_info__last_name",
        "personal_info__identification",
        "employment_details__job_title__name",
    )
    list_display = (
        get_full_name,
        "personal_info__identification",
        "employment_details__job_title",
    )
    # list_filter = ("campaign",)
    list_per_page = 25
    list_max_show_all = 100
    # ordering = ("first_name", "last_name", "campaign")
    # fieldsets = (
    #     (
    #         "Información Personal",
    #         {
    #             "fields": (
    #                 ("photo_thumbnail", "photo"),
    #                 ("document_type", "identification"),
    #                 ("expedition_place", "expedition_date"),
    #                 ("first_name", "last_name"),
    #                 ("email", "corporate_email"),
    #                 ("birth_date", "gender"),
    #                 ("civil_status", "sons"),
    #                 ("responsible_persons", "stratum"),
    #                 ("fixed_phone", "cell_phone"),
    #                 ("emergency_contact", "emergency_relationship", "emergency_phone"),
    #                 "rh",
    #             )
    #         },
    #     ),
    #     (
    #         "Dirección",
    #         {"fields": (("locality", "address", "neighborhood"),)},
    #     ),
    #     (
    #         "Información educativa",
    #         {"fields": (("education_level", "title", "ongoing_studies"),)},
    #     ),
    #     (
    #         "Información Laboral",
    #         {
    #             "fields": (
    #                 ("affiliation_date", "health_provider", "legacy_health_provider"),
    #                 ("pension_fund", "compensation_fund", "saving_fund"),
    #                 ("payroll_account", "bank"),
    #                 (
    #                     "headquarter",
    #                     "management",
    #                     "campaign",
    #                 ),
    #                 ("appointment_date", "legacy_appointment_date"),
    #                 ("business_area", "job_title"),
    #                 "contract_type",
    #                 "entry_date",
    #                 ("salary", "transportation_allowance"),
    #                 ("remote_work_application_date", "remote_work"),
    #                 ("shirt_size", "pant_size", "shoe_size"),
    #             )
    #         },
    #     ),
    #     (
    #         "Acciones Disciplinarias",
    #         {
    #             "fields": (
    #                 (
    #                     "memo_1",
    #                     "memo_2",
    #                     "memo_3",
    #                 )
    #             )
    #         },
    #     ),
    #     (
    #         "Información de retiro",
    #         {
    #             "fields": (
    #                 ("termination_date", "termination_type", "termination_reason"),
    #                 ("status", "rehire_eligibility"),
    #             )
    #         },
    #     ),
    # )

    def has_delete_permission(self, request, obj=None):
        return False
