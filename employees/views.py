import os
from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView

from administration.models import *
from employees.forms import (
    ContactInformationForm,
    EducationForm,
    EmergencyContactForm,
    EmployeeForm,
    EmploymentDetailsForm,
    PersonalInformationForm,
    TerminationDetailsForm,
)

from .models import (
    ContactInformation,
    Education,
    EmergencyContact,
    Employee,
    EmploymentDetails,
    PersonalInformation,
    TerminationDetails,
)


def parse_date(date_str):
    """Parses a date string."""
    if not date_str:
        return None
    if date_str == "1900-01-01":
        return date_str
    date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return date_obj.strftime("%Y-%m-%d")


# ! Uncomment this function to use it
def get_employees_from_db(request):
    """Gets employees from an external API and saves them in bulk with related models."""

    # Clear previous data
    Employee.objects.all().delete()
    PersonalInformation.objects.all().delete()
    ContactInformation.objects.all().delete()
    EmergencyContact.objects.all().delete()
    Education.objects.all().delete()
    EmploymentDetails.objects.all().delete()
    TerminationDetails.objects.all().delete()
    Bank.objects.all().delete()
    Campaign.objects.all().delete()
    CompensationFund.objects.all().delete()
    HealthProvider.objects.all().delete()
    Headquarter.objects.all().delete()
    JobTitle.objects.all().delete()
    Locality.objects.all().delete()
    Management.objects.all().delete()
    PensionFund.objects.all().delete()
    SavingFund.objects.all().delete()

    # Fetch employee data from API
    cookie_token = "a19ea262-8e38-4041-8352-0cada99252b7"
    request.COOKIES["StaffNet"] = cookie_token
    response = requests.post(
        "https://staffnet-api.cyc-bpo.com/search_employees", cookies=request.COOKIES
    )
    employees = response.json()

    if employees.get("error"):
        return JsonResponse({"StaffNet-old error": employees["error"]}, status=500)

    # Prepare lists for bulk insert
    personal_info_list = []
    contact_info_list = []
    emergency_contact_list = []
    education_list = []
    employment_details_list = []
    termination_details_list = []
    employees_list = []

    for employee_data in employees["info"]["data"]:
        # Prepare and clean data for each related model
        # Set some columns in None if they are empty
        for key in employee_data:
            key = key.lower()
            employee_data[key] = (
                employee_data[key].strip()
                if employee_data[key] and type(employee_data[key]) == str
                else employee_data[key]
            )
            if (
                not employee_data[key]
                or employee_data[key] == "null"
                or employee_data[key] == ""
            ):
                employee_data[key] = None
            if key == "parentesco" and employee_data[key] == "HERMANO (A)":
                employee_data[key] = "HERMANO(A)"
            elif key == "correo" and employee_data[key] == "#N/D":
                employee_data[key] = None
            elif key == "tel_contacto" and employee_data[key]:
                if "-" in employee_data[key]:
                    employee_data[key] = employee_data[key].split("-")[1].strip()
                elif "//" in employee_data[key]:
                    employee_data[key] = employee_data[key].split("//")[1].strip()
                elif employee_data[key] == "320896082EVELIN M2":
                    employee_data[key] = "320896082"
            elif key == "celular" and employee_data[key]:
                if "-" in employee_data[key]:
                    employee_data[key] = employee_data[key].split("-")[1].strip()
                elif "/" in employee_data[key]:
                    employee_data[key] = employee_data[key].split("/")[1].strip()
        if (
            employee_data["correo"] == "PABLO.CASTANEDA@CYC-BPO.COM"
            and employee_data["correo_corporativo"] == "YARIME.GIRALDO@CYC-BPO.COM"
        ):
            employee_data["correo"] = "PABLO.CASTANEDA+2@CYC-BPO.COM"
        elif (
            employee_data["correo"] == "YINETHROMERO0705@GMAIL.COM"
            and employee_data["nombres"] == "LAURA VALENTINA"
        ):
            employee_data["correo"] = "YINETHROMERO0705+LAURA@GMAIL.COM"
        elif (
            employee_data["correo"] == "CARITO8827@HOTMAIL.COM"
            and employee_data["apellidos"] == "MORALES VALDES"
        ):
            employee_data["correo"] = "CARITO8827+ERIKA@HOTMAIL.COM"
        elif (
            employee_data["correo"] == "LIYI0311@HOTMAIL.COM"
            and employee_data["nombres"] == "ZULEY NATALIA"
        ):
            employee_data["correo"] = "LIYI0311+ZULEY@HOTMAIL.COM"
        if (
            employee_data["usuario_windows"]
            and employee_data["usuario_windows"].lower() == "no"
        ):
            employee_data["usuario_windows"] = None
        elif (
            employee_data["usuario_windows"]
            and employee_data["usuario_windows"].lower() == "daniel.ramirez"
            and employee_data["cedula"] == 1012328078
        ):
            employee_data["usuario_windows"] = None
        if (
            employee_data["memorando_1"]
            and employee_data["memorando_1"].lower() == "#N/D"
        ):
            employee_data["memorando_1"] = None
        if (
            employee_data["memorando_2"]
            and employee_data["memorando_2"].lower() == "#N/D"
        ):
            employee_data["memorando_2"] = None
        if (
            employee_data["memorando_3"]
            and employee_data["memorando_3"].lower() == "#N/D"
        ):
            employee_data["memorando_3"] = None
        if employee_data["fecha_nombramiento_legado"] == "#N/D":
            employee_data["fecha_nombramiento_legado"] = None
        if employee_data["campana_general"] == "YANBAL - VILLAVICENCIO":
            employee_data["campana_general"] = "YANBAL VILLAVICENCIO"
        elif (
            employee_data["campana_general"]
            and employee_data["campana_general"] == "PAY U"
            or employee_data["campana_general"] == "PAY-U"
        ):
            employee_data["campana_general"] = "PAYU"
        if employee_data["caja_compensacion"] == "N/A":
            employee_data["caja_compensacion"] = "No especificada"
        if employee_data["eps"] == "ECOOPOS EPS":
            employee_data["eps"] = "ECOOPSOS EPS"
        elif employee_data["eps"] == "MEDIMAS":
            employee_data["eps"] = "MEDIMAS EPS"
        if employee_data["cargo"] == "DIRECTOR(A) DE INVESTIGACION":
            employee_data["cargo"] = "DIRECTOR(A) DE INVESTIGACIONES"
        if employee_data["pension"] == "N/A":
            employee_data["pension"] = "No especificada"
        if employee_data["cesantias"] == "N/A":
            employee_data["cesantias"] = "No especificada"
        photo_exists = os.path.exists(
            settings.BASE_DIR
            / "media"
            / f"employees/photos/{employee_data['cedula']}.webp"
        )

        # Personal Information
        print(employee_data["cedula"])
        personal_info = PersonalInformation(
            photo=(
                f"employees/photos/{employee_data['cedula']}.webp"
                if photo_exists
                else None
            ),
            identification=int(employee_data.get("cedula", 0)),
            last_name=employee_data.get("apellidos"),
            first_name=employee_data.get("nombres"),
            document_type=employee_data.get("tipo_documento"),
            birth_date=parse_date(employee_data.get("fecha_nacimiento")),
            expedition_place=employee_data.get("lugar_expedicion") or "No especificado",
            expedition_date=parse_date(
                employee_data.get("fecha_expedicion") or "1900-01-01"
            ),
            gender="M" if employee_data.get("genero") == "MASCULINO" else "F",
            rh=employee_data.get("rh") or "O+",
            civil_status=employee_data.get("estado_civil"),
            sons=employee_data.get("hijos") or 0,
            responsible_persons=employee_data.get("personas_a_cargo") or 0,
            shirt_size=employee_data.get("talla_camisa") or "N/A",
            pant_size=employee_data.get("talla_pantalon") or 28,
            shoe_size=employee_data.get("talla_zapatos") or 38,
            stratum=employee_data.get("estrato") or 2,
        )
        personal_info_list.append(personal_info)

        contact_info = ContactInformation(
            fixed_phone=employee_data.get("tel_fijo"),
            cell_phone=employee_data.get("celular") or 0,
            email=employee_data.get("correo"),
            corporate_email=employee_data.get("correo_corporativo"),
            address=employee_data.get("direccion") or "No especificada",
            neighborhood=employee_data.get("barrio") or "No especificado",
            locality=Locality.objects.get_or_create(
                name=employee_data.get("localidad") or "No especificada"
            )[0],
        )
        contact_info_list.append(contact_info)

        # Emergency Contact
        emergency_contact = EmergencyContact(
            name=employee_data.get("contacto_emergencia") or "No especificado",
            relationship=employee_data.get("parentesco") or "OTRO",
            phone=employee_data.get("tel_contacto") or "No especificado",
        )
        emergency_contact_list.append(emergency_contact)

        # Education Information
        education = Education(
            education_level=employee_data.get("nivel_escolaridad"),
            title=employee_data.get("profesion"),
            ongoing_studies=bool(employee_data.get("estudios_en_curso")),
        )
        education_list.append(education)

        # Employment Details
        employment_details = EmploymentDetails(
            affiliation_date=parse_date(
                employee_data.get("fecha_afiliacion_eps")
                or employee_data.get("fecha_ingreso")
            ),
            health_provider=HealthProvider.objects.get_or_create(
                name=employee_data.get("eps") or "No especificada"
            )[0],
            legacy_health_provider=employee_data.get("cambio_eps_legado"),
            pension_fund=PensionFund.objects.get_or_create(
                name=employee_data.get("pension") or "No especificada"
            )[0],
            compensation_fund=CompensationFund.objects.get_or_create(
                name=employee_data.get("caja_compensacion") or "No especificada"
            )[0],
            saving_fund=SavingFund.objects.get_or_create(
                name=employee_data.get("cesantias") or "No especificada"
            )[0],
            payroll_account=employee_data.get("cuenta_nomina") or 0,
            bank=Bank.objects.get_or_create(
                name=employee_data.get("banco") or "BANCO CAJA SOCIAL"
            )[0],
            headquarter=Headquarter.objects.get_or_create(
                name=employee_data.get("sede") or "No especificada"
            )[0],
            job_title=JobTitle.objects.get_or_create(name=employee_data.get("cargo"))[
                0
            ],
            appointment_date=parse_date(employee_data.get("fecha_nombramiento")),
            legacy_appointment_date=employee_data.get("fecha_nombramiento_legado"),
            management=Management.objects.get_or_create(
                name=employee_data.get("gerencia") or "No especificada"
            )[0],
            campaign=Campaign.objects.get_or_create(
                name=employee_data.get("campana_general")
            )[0],
            business_area=employee_data.get("area_negocio"),
            contract_type=employee_data.get("tipo_contrato") or "OBRA O LABOR",
            entry_date=parse_date(employee_data.get("fecha_ingreso")),
            salary=employee_data.get("salario"),
            transportation_allowance=employee_data.get("subsidio_transporte") or 0,
            remote_work_application_date=parse_date(
                "1900-01-01"
                if employee_data.get("aplica_teletrabajo")
                and not employee_data.get("fecha_aplica_teletrabajo")
                else employee_data.get("fecha_aplica_teletrabajo")
            ),
            remote_work=bool(
                True
                if employee_data.get("fecha_aplica_teletrabajo")
                or employee_data.get("aplica_teletrabajo")
                else False
            ),
            windows_user=employee_data.get("usuario_windows"),
        )
        employment_details_list.append(employment_details)

        # Termination Details
        termination_details = TerminationDetails(
            termination_date=parse_date(employee_data.get("fecha_retiro")),
            termination_type=employee_data.get("tipo_retiro"),
            termination_reason=employee_data.get("motivo_retiro"),
            rehire_eligibility=(
                # ! Check that this work
                employee_data.get("aplica_recontratacion")
                if employee_data.get("aplica_recontratacion") is not None
                else True
            ),
        )
        termination_details_list.append(termination_details)

    # Can't bulk create related models because they have foreign keys
    for personal_info in personal_info_list:
        personal_info.clean()
        personal_info.save()
    for contact_info in contact_info_list:
        contact_info.clean()
        contact_info.save()
    for emergency_contact in emergency_contact_list:
        emergency_contact.clean()
        emergency_contact.save()
    for education in education_list:
        education.clean()
        education.save()
    for employment_details in employment_details_list:
        employment_details.clean()
        employment_details.save()
    for termination_details in termination_details_list:
        termination_details.clean()
        termination_details.save()

    # Retrieve created records and link to Employee
    for i in range(len(personal_info_list)):
        employee = Employee(
            personal_info=personal_info_list[i],
            contact_info=contact_info_list[i],
            emergency_contact=emergency_contact_list[i],
            education=education_list[i],
            employment_details=employment_details_list[i],
            termination_details=termination_details_list[i],
            status=True if not termination_details_list[i].termination_date else False,
        )
        employees_list.append(employee)

    # Bulk create employees
    Employee.objects.bulk_create(employees_list)

    return JsonResponse({"message": "Employees saved to the database."})


class EmployeeListView(ListView):
    """Employee list view."""

    model = Employee
    context_object_name = "employees"
    paginate_by = 11

    def get_queryset(self):
        """Get the queryset."""
        queryset = Employee.objects.only(
            "personal_info__first_name",
            "personal_info__last_name",
            "personal_info__identification",
            "employment_details__job_title",
            "status",
        ).order_by("personal_info__first_name", "personal_info__last_name")
        query = self.request.GET.get("query")
        if query:
            # queryset = queryset.annotate(
            #     full_name=Concat(
            #         "personal_info__first_name",
            #         Value(" "),
            #         "personal_info__last_name",
            #     )
            # )
            # Filter the queryset based on the search query
            queryset = queryset.filter(
                # Q(full_name__icontains=query) |
                Q(personal_info__first_name__icontains=query)
                | Q(personal_info__last_name__icontains=query)
                | Q(personal_info__identification__icontains=query)
                | Q(employment_details__job_title__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Get the context data."""
        context = super().get_context_data(**kwargs)
        context["query"] = (
            self.request.GET.get("query") if self.request.GET.get("query") else ""
        )
        return context


class EmployeeDetailView(View):
    """Employee detail view."""

    template_name = "employees/employee_detail.html"

    def get_forms(self, employee):
        """Helper method to instantiate forms."""
        data = {
            "employee_form": EmployeeForm(instance=employee),
            "personal_info_form": PersonalInformationForm(
                instance=employee.personal_info
            ),
            "contact_info_form": ContactInformationForm(instance=employee.contact_info),
            "emergency_contact_form": EmergencyContactForm(
                instance=employee.emergency_contact
            ),
            "education_form": EducationForm(instance=employee.education),
            "employment_details_form": EmploymentDetailsForm(
                instance=employee.employment_details
            ),
            "termination_details_form": TerminationDetailsForm(
                instance=employee.termination_details
            ),
        }
        for field_name, field in data["employment_details_form"].fields.items():
            print(f"{field_name}: {field.initial}")
        return data

    def get(self, request, pk, *args, **kwargs):
        employee = get_object_or_404(Employee, pk=pk)
        forms = self.get_forms(employee)
        return render(request, self.template_name, {**forms, "employee": employee})


class CreateEmployeeView(View):
    template_name = "employees/employee_form.html"

    def get_forms(self):
        """Helper method to instantiate forms."""
        return {
            "employee_form": EmployeeForm(),
            "personal_info_form": PersonalInformationForm(),
            "contact_info_form": ContactInformationForm(),
            "emergency_contact_form": EmergencyContactForm(),
            "education_form": EducationForm(),
            "employment_details_form": EmploymentDetailsForm(),
            "termination_details_form": TerminationDetailsForm(),
        }

    def post_forms(self, data, files):
        """Helper method to instantiate forms with POST data."""
        return {
            "employee_form": EmployeeForm(data),
            "personal_info_form": PersonalInformationForm(data, files),
            "contact_info_form": ContactInformationForm(data),
            "emergency_contact_form": EmergencyContactForm(data),
            "education_form": EducationForm(data),
            "employment_details_form": EmploymentDetailsForm(data),
            "termination_details_form": TerminationDetailsForm(data),
        }

    def get(self, request, *args, **kwargs):
        forms = self.get_forms()
        return render(request, self.template_name, {**forms, "view_type": "Crear"})

    def post(self, request, *args, **kwargs):
        forms = self.post_forms(request.POST, request.FILES)

        # Check if all forms are valid
        if all(form.is_valid() for form in forms.values()):
            # Save forms and set relationships
            employee = forms["employee_form"].save(commit=False)
            employee.personal_info = forms["personal_info_form"].save()
            employee.contact_info = forms["contact_info_form"].save()
            employee.emergency_contact = forms["emergency_contact_form"].save()
            employee.education = forms["education_form"].save()
            employee.employment_details = forms["employment_details_form"].save()
            employee.termination_details = forms["termination_details_form"].save()
            employee.status = True  # Active by default
            employee.save()
            return redirect("employees-list")

        return render(request, self.template_name, {**forms, "view_type": "Crear"})


# class UpdateEmployeeView(View):
#     template_name = "employees/employee_form.html"

#     def get_forms(self, employee):
#         """Helper method to instantiate forms."""
#         return {
#             "employee_form": EmployeeForm(instance=employee),
#             "personal_info_form": PersonalInformationForm(instance=employee.personal_info),
#             "contact_info_form": ContactInformationForm(instance=employee.contact_info),
#             "emergency_contact_form": EmergencyContactForm(
#                 instance=employee.emergency_contact
#             ),
#             "education_form": EducationForm(instance=employee.education),
#             "employment_details_form": EmploymentDetailsForm(
#                 instance=employee.employment_details
#             ),
#             "termination_details_form": TerminationDetailsForm(
#                 instance=employee.termination_details
#             ),
#         }

#     def post_forms(self, data, files, employee):
#         """Helper method to instantiate forms with POST data."""
#         return {
#             "employee_form": EmployeeForm(data, instance=employee),
#             "personal_info_form": PersonalInformationForm(data, files, instance=employee.personal_info),
#             "contact_info_form": ContactInformationForm(data, instance=employee.contact_info),
#             "emergency_contact_form": EmergencyContactForm(data, instance=employee.emergency_contact),
#             "education_form": EducationForm(data, instance=employee.education),
#             "employment_details_form": EmploymentDetailsForm(data, instance=employee.employment_details),
#             "termination_details_form": TerminationDetailsForm(data, instance=employee.termination_details),
#         }

#     def get(self, request, pk, *args, **kwargs):
#         employee = get_object_or_404(Employee, pk=pk)
#         forms = self.get_forms(employee)
#         return render(request, self.template_name, {**forms, "view_type": "Editar"})

#     def post(self, request, pk, *args, **kwargs):
#         employee = get_object_or_404(Employee, pk=pk)
#         forms = self.post_forms(request.POST, request.FILES, employee)

#         # Check if all forms are valid
#         if all(form.is_valid() for form in forms.values()):
#             # Save forms and set relationships
#             employee = forms["employee_form"].save(commit=False)
#             employee.personal_info = forms["personal_info_form"].save()
#             employee.contact_info = forms["contact_info_form"].save()
#             employee.emergency_contact = forms["emergency_contact_form"].save()
#             employee.education = forms["education_form"].save()
#             employee.employment_details = forms["employment_details_form"].save()
#             employee.termination_details = forms["termination_details_form"].save()
#             employee.save()
#             return redirect("employees-list")
#         else:
#             for name, form in forms.items():
#                 if not form.is_valid():
#                     print(f"Errors in {name}: {form.errors}")

#         return render(request, self.template_name, {**forms, "view_type": "Editar"})
