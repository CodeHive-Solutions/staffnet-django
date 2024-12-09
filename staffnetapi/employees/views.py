import os
from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

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
    cookie_token = "7ca6b0de-2d43-4ab9-967b-01ffdabbb4d8"
    request.COOKIES["StaffNet"] = cookie_token
    response = requests.post(
        "https://staffnet-api.cyc-bpo.com/search_employees", cookies=request.COOKIES
    )
    employees = response.json()

    if employees.get("error"):
        return JsonResponse({"error": employees["error"]}, status=500)

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
            / f"employees/profile_pictures/{employee_data['cedula']}.webp"
        )

        # Personal Information
        personal_info = PersonalInformation(
            # photo=f"employees/profile_pictures/{employee_data['cedula']}.webp"
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
            remote_work=bool(employee_data.get("aplica_teletrabajo")),
            remote_work_application_date=parse_date(
                employee_data.get("fecha_aplica_teletrabajo")
            ),
            windows_user=employee_data.get("usuario_windows"),
        )
        employment_details_list.append(employment_details)

        # Termination Details
        termination_details = TerminationDetails(
            termination_date=None,
            termination_type=None,
            termination_reason=None,
            rehire_eligibility=True,
        )
        termination_details_list.append(termination_details)

    # Can't bulk create related models because they have foreign keys
    for personal_info in personal_info_list:
        personal_info.save()
    for contact_info in contact_info_list:
        contact_info.save()
    for emergency_contact in emergency_contact_list:
        emergency_contact.save()
    for education in education_list:
        education.save()
    for employment_details in employment_details_list:
        employment_details.save()
    for termination_details in termination_details_list:
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
            status=True,
        )
        employees_list.append(employee)

    # Bulk create employees
    Employee.objects.bulk_create(employees_list)

    return JsonResponse({"message": "Employees saved to the database."})


# def get_employees_from_db(request):
#     """Gets the employees from the external API."""
#     # First delete all records from the models
#     Employee.objects.all().delete()
#     Bank.objects.all().delete()
#     Campaign.objects.all().delete()
#     CompensationFund.objects.all().delete()
#     HealthProvider.objects.all().delete()
#     Headquarter.objects.all().delete()
#     JobTitle.objects.all().delete()
#     Locality.objects.all().delete()
#     Management.objects.all().delete()
#     PensionFund.objects.all().delete()
#     SavingFund.objects.all().delete()
#     # Set the cookie token
#     cookie_token = "7ca6b0de-2d43-4ab9-967b-01ffdabbb4d8"
#     # set the cookie
#     request.COOKIES["StaffNet"] = cookie_token
#     # Request the employees from the external API using the cookie token
#     response = requests.post(
#         "https://staffnet-api.cyc-bpo.com/search_employees",
#         cookies=request.COOKIES,
#     )
#     employees = response.json()
#     if employees.get("error"):
#         return JsonResponse({"error": employees["error"]}, status=500)
#     employees_batch = []
#     # Save the employees to the database
#     for employee_data in employees["info"]["data"]:

#     # Set some columns in None if they are empty
#     for key in employee_data:
#         key = key.lower()
#         employee_data[key] = (
#             employee_data[key].strip()
#             if employee_data[key] and type(employee_data[key]) == str
#             else employee_data[key]
#         )
#         if (
#             not employee_data[key]
#             or employee_data[key] == "null"
#             or employee_data[key] == ""
#         ):
#             employee_data[key] = None
#         if key == "parentesco" and employee_data[key] == "HERMANO (A)":
#             employee_data[key] = "HERMANO(A)"
#         elif key == "correo" and employee_data[key] == "#N/D":
#             employee_data[key] = None
#         elif key == "tel_contacto" and employee_data[key]:
#             if "-" in employee_data[key]:
#                 employee_data[key] = employee_data[key].split("-")[1].strip()
#             elif "//" in employee_data[key]:
#                 employee_data[key] = employee_data[key].split("//")[1].strip()
#             elif employee_data[key] == "320896082EVELIN M2":
#                 employee_data[key] = "320896082"
#         elif key == "celular" and employee_data[key]:
#             if "-" in employee_data[key]:
#                 employee_data[key] = employee_data[key].split("-")[1].strip()
#             elif "/" in employee_data[key]:
#                 employee_data[key] = employee_data[key].split("/")[1].strip()
#     if (
#         employee_data["correo"] == "PABLO.CASTANEDA@CYC-BPO.COM"
#         and employee_data["correo_corporativo"] == "YARIME.GIRALDO@CYC-BPO.COM"
#     ):
#         employee_data["correo"] = "PABLO.CASTANEDA+2@CYC-BPO.COM"
#     elif (
#         employee_data["correo"] == "YINETHROMERO0705@GMAIL.COM"
#         and employee_data["nombres"] == "LAURA VALENTINA"
#     ):
#         employee_data["correo"] = "YINETHROMERO0705+LAURA@GMAIL.COM"
#     elif (
#         employee_data["correo"] == "CARITO8827@HOTMAIL.COM"
#         and employee_data["apellidos"] == "MORALES VALDES"
#     ):
#         employee_data["correo"] = "CARITO8827+ERIKA@HOTMAIL.COM"
#     elif (
#         employee_data["correo"] == "LIYI0311@HOTMAIL.COM"
#         and employee_data["nombres"] == "ZULEY NATALIA"
#     ):
#         employee_data["correo"] = "LIYI0311+ZULEY@HOTMAIL.COM"
#     if (
#         employee_data["usuario_windows"]
#         and employee_data["usuario_windows"].lower() == "no"
#     ):
#         employee_data["usuario_windows"] = None
#     elif (
#         employee_data["usuario_windows"]
#         and employee_data["usuario_windows"].lower() == "daniel.ramirez"
#         and employee_data["cedula"] == 1012328078
#     ):
#         employee_data["usuario_windows"] = None
#     if (
#         employee_data["memorando_1"]
#         and employee_data["memorando_1"].lower() == "#N/D"
#     ):
#         employee_data["memorando_1"] = None
#     if (
#         employee_data["memorando_2"]
#         and employee_data["memorando_2"].lower() == "#N/D"
#     ):
#         employee_data["memorando_2"] = None
#     if (
#         employee_data["memorando_3"]
#         and employee_data["memorando_3"].lower() == "#N/D"
#     ):
#         employee_data["memorando_3"] = None
#     if employee_data["fecha_nombramiento_legado"] == "#N/D":
#         employee_data["fecha_nombramiento_legado"] = None
#     if employee_data["campana_general"] == "YANBAL - VILLAVICENCIO":
#         employee_data["campana_general"] = "YANBAL VILLAVICENCIO"
#     elif (
#         employee_data["campana_general"]
#         and employee_data["campana_general"] == "PAY U"
#         or employee_data["campana_general"] == "PAY-U"
#     ):
#         employee_data["campana_general"] = "PAYU"
#     if employee_data["caja_compensacion"] == "N/A":
#         employee_data["caja_compensacion"] = "No especificada"
#     if employee_data["eps"] == "ECOOPOS EPS":
#         employee_data["eps"] = "ECOOPSOS EPS"
#     elif employee_data["eps"] == "MEDIMAS":
#         employee_data["eps"] = "MEDIMAS EPS"
#     if employee_data["cargo"] == "DIRECTOR(A) DE INVESTIGACION":
#         employee_data["cargo"] = "DIRECTOR(A) DE INVESTIGACIONES"
#     if employee_data["pension"] == "N/A":
#         employee_data["pension"] = "No especificada"
#     if employee_data["cesantias"] == "N/A":
#         employee_data["cesantias"] = "No especificada"
#     photo_exists = os.path.exists(
#         settings.BASE_DIR
#         / "media"
#         / f"employees/profile_pictures/{employee_data['cedula']}.webp"
#     )
#     employees_batch.append(
#         Employee(
#             identification=int(employee_data["cedula"]),
#             last_name=employee_data["apellidos"],
#             first_name=employee_data["nombres"],
#             document_type=employee_data["tipo_documento"],
#             birth_date=parse_date(employee_data["fecha_nacimiento"]),
#             expedition_place=employee_data["lugar_expedicion"] or "No especificado",
#             expedition_date=parse_date(
#                 # ! Delete after testing
#                 employee_data["fecha_expedicion"]
#                 or "Mon, 01 Jan 1900 00:00:00 GMT"
#             ),
#             gender="M" if employee_data["genero"] == "MASCULINO" else "F",
#             rh=employee_data["rh"] or "O+",
#             civil_status=employee_data["estado_civil"],
#             sons=employee_data["hijos"] or 0,
#             responsible_persons=employee_data["personas_a_cargo"] or 0,
#             stratum=employee_data["estrato"] or 2,
#             fixed_phone=employee_data["tel_fijo"],
#             cell_phone=employee_data["celular"] or 0,
#             email=employee_data["correo"],
#             corporate_email=employee_data["correo_corporativo"],
#             address=employee_data["direccion"] or "No especificada",
#             neighborhood=employee_data["barrio"] or "No especificado",
#             locality=Locality.objects.get_or_create(
#                 name=employee_data["localidad"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             emergency_contact=employee_data["contacto_emergencia"]
#             or "No especificado",
#             emergency_relationship=employee_data["parentesco"] or "OTRO",
#             emergency_phone=employee_data["tel_contacto"] or "No especificado",
#             education_level=employee_data["nivel_escolaridad"],
#             title=employee_data["profesion"],
#             ongoing_studies=bool(employee_data["estudios_en_curso"]),
#             affiliation_date=parse_date(
#                 employee_data["fecha_afiliacion_eps"]
#                 or employee_data["fecha_ingreso"]
#             ),
#             health_provider=HealthProvider.objects.get_or_create(
#                 name=employee_data["eps"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             legacy_health_provider=employee_data["cambio_eps_legado"],
#             pension_fund=PensionFund.objects.get_or_create(
#                 name=employee_data["pension"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             compensation_fund=CompensationFund.objects.get_or_create(
#                 name=employee_data["caja_compensacion"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             saving_fund=SavingFund.objects.get_or_create(
#                 name=employee_data["cesantias"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             payroll_account=employee_data["cuenta_nomina"] or 0,
#             bank=Bank.objects.get_or_create(
#                 name=employee_data["banco"] or "BANCO CAJA SOCIAL"
#             )[
#                 0
#             ],  # Fetching from database
#             headquarter=Headquarter.objects.get_or_create(
#                 name=employee_data["sede"] or "No especificada"
#             )[
#                 0
#             ],  # Fetching from database
#             job_title=JobTitle.objects.get_or_create(name=employee_data["cargo"])[
#                 0
#             ],  # Fetching from database
#             appointment_date=(
#                 parse_date(employee_data["fecha_nombramiento"])
#                 if employee_data["fecha_nombramiento"]
#                 else None
#             ),
#             legacy_appointment_date=(employee_data["fecha_nombramiento_legado"]),
#             management=Management.objects.get_or_create(
#                 name=employee_data["gerencia"] or "BANCO AGRARIO"
#             )[
#                 0
#             ],  # Fetching from database
#             campaign=Campaign.objects.get_or_create(
#                 name=employee_data["campana_general"]
#             )[
#                 0
#             ],  # Fetching from database
#             business_area=employee_data["area_negocio"],
#             contract_type=employee_data["tipo_contrato"] or "OBRA O LABOR",
#             entry_date=parse_date(employee_data["fecha_ingreso"]),
#             salary=employee_data["salario"],
#             transportation_allowance=employee_data["subsidio_transporte"] or 0,
#             remote_work=bool(employee_data["aplica_teletrabajo"]),
#             remote_work_application_date=(
#                 parse_date(employee_data["fecha_aplica_teletrabajo"])
#                 if employee_data["fecha_aplica_teletrabajo"]
#                 else None
#             ),
#             shirt_size=employee_data.get("talla_camisa"),
#             pant_size=employee_data.get("talla_pantalon"),
#             shoe_size=employee_data.get("talla_zapatos"),
#             windows_user=employee_data.get("usuario_windows"),
#             memo_1=employee_data.get("memorando_1"),
#             memo_2=employee_data.get("memorando_2"),
#             memo_3=employee_data.get("memorando_3"),
#             photo=(
#                 f"employees/photos/{employee_data['cedula']}.webp"
#                 if photo_exists
#                 else None
#             ),
#         )
#     )
# Employee.objects.bulk_create(employees_batch)
# return JsonResponse({"message": "Employees saved to the database."})


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
        query = self.request.GET.get("q")
        if query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(
                Q(personal_info__first_name__icontains=query)
                | Q(personal_info__last_name__icontains=query)
                | Q(personal_info__identification__icontains=query)
                | Q(employment_details__job_title__name__icontains=query)
            )
        return queryset


class EmployeeDetailView(DetailView):
    """Employee detail view."""

    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"

    def get_context_data(self, **kwargs):
        """Get the context data."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Employee Detail"
        employee = self.get_object()
        context["fields"] = model_to_dict(employee)
        return context


def employee_update_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect("employees-list")
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request, "employees/employee_update.html", {"form": form, "employee": employee}
    )


class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy("employee_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_type"] = "Update"
        context["button_label"] = "Update"

        return context


# class EmployeeCreateView(CreateView):
#     model = Employee
#     form_class = EmployeeForm
#     # template_name = "employees/test_employee.html"
#     success_url = reverse_lazy("employees-list")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["view_type"] = "Crear"
#         context['form'] = EmployeeForm(instance=self.object) if self.object else EmployeeForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         # Process forms as in your existing code
#         forms = {
#             "personal_information_form": PersonalInformationForm(request.POST),
#             "contact_information_form": ContactInformationForm(request.POST),
#             "emergency_contact_form": EmergencyContactForm(request.POST),
#             "education_form": EducationForm(request.POST),
#             "employment_details_form": EmploymentDetailsForm(request.POST),
#             "termination_details_form": TerminationDetailsForm(request.POST),
#         }

#         all_valid = all(form.is_valid() for form in forms.values())

#         if all_valid:
#             personal_information = forms["personal_information_form"].save()
#             contact_information = forms["contact_information_form"].save()
#             emergency_contact = forms["emergency_contact_form"].save()
#             education = forms["education_form"].save()
#             employment_details = forms["employment_details_form"].save()
#             termination_details = forms["termination_details_form"].save()

#             employee = Employee(
#                 personal_info=personal_information,
#                 contact_info=contact_information,
#                 emergency_contact=emergency_contact,
#                 education=education,
#                 employment_details=employment_details,
#                 termination_details=termination_details,
#             )
#             employee.save()
#             return redirect("employees-list")
#         else:
#             data = {
#                 "view_type": "Crear",
#                 "forms": forms,
#             }
#             return render(
#                 request,
#                 "employees/employee_form.html",
#                 data,
#             )

#     # ! This approach is close to work but i don't like it
#     # def post(self, request, *args, **kwargs):
#     #     print("POST")
#     #     personal_information_form = PersonalInformationForm(request.POST)
#     #     contact_information_form = ContactInformationForm(request.POST)
#     #     emergency_contact_form = EmergencyContactForm(request.POST)
#     #     education_form = EducationForm(request.POST)
#     #     employment_details_form = EmploymentDetailsForm(request.POST)
#     #     termination_details_form = TerminationDetailsForm(request.POST)

#     #     if (
#     #         personal_information_form.is_valid()
#     #         and contact_information_form.is_valid()
#     #         and emergency_contact_form.is_valid()
#     #         and education_form.is_valid()
#     #         and employment_details_form.is_valid()
#     #         and termination_details_form.is_valid()
#     #     ):
#     #         personal_information = personal_information_form.save()
#     #         contact_information = contact_information_form.save()
#     #         emergency_contact = emergency_contact_form.save()
#     #         education = education_form.save()
#     #         employment_details = employment_details_form.save()
#     #         termination_details = termination_details_form.save()

#     #         employee = Employee(
#     #             personal_info=personal_information,
#     #             contact_info=contact_information,
#     #             emergency_contact=emergency_contact,
#     #             education=education,
#     #             employment_details=employment_details,
#     #             termination_details=termination_details,
#     #         )
#     #         employee.save()
#     #         return redirect("employees-list")
#     #     else:
#     #         print(personal_information_form.errors)
#     #         print(contact_information_form.errors)
#     #         print(emergency_contact_form.errors)
#     #         print(education_form.errors)
#     #         print(employment_details_form.errors)
#     #         print(termination_details_form.errors)
#     #         return render(
#     #             request,
#     #             "employees/employee_form.html",
#     #             {
#     #                 "view_type": "Crear",
#     #                 "form": EmployeeForm(),
#     #                 "personal_information_form": personal_information_form,
#     #                 "contact_information_form": contact_information_form,
#     #                 "emergency_contact_form": emergency_contact_form,
#     #                 "education_form": education_form,
#     #                 "employment_details_form": employment_details_form,
#     #                 "termination_details_form": termination_details_form,
#     #             },
#     #         )

from django.shortcuts import redirect, render


def create_employee(request):
    if request.method == "POST":
        # Instantiate all forms with POST data
        employee_form = EmployeeForm(request.POST)
        personal_info_form = PersonalInformationForm(request.POST, request.FILES)
        contact_info_form = ContactInformationForm(request.POST)
        emergency_contact_form = EmergencyContactForm(request.POST)
        education_form = EducationForm(request.POST)
        employment_details_form = EmploymentDetailsForm(request.POST)
        termination_details_form = TerminationDetailsForm(request.POST)

        if (
            employee_form.is_valid()
            and personal_info_form.is_valid()
            and contact_info_form.is_valid()
            and emergency_contact_form.is_valid()
            and education_form.is_valid()
            and employment_details_form.is_valid()
            and termination_details_form.is_valid()
        ):
            print("Exitoso")
            # Save the Employee and related models
            employee = employee_form.save(commit=False)
            personal_info = personal_info_form.save()
            contact_info = contact_info_form.save()
            emergency_contact = emergency_contact_form.save()
            education = education_form.save()
            employment_details = employment_details_form.save()
            termination_details = termination_details_form.save()

            # Set relationships
            employee.personal_info = personal_info
            employee.contact_info = contact_info
            employee.emergency_contact = emergency_contact
            employee.education = education
            employee.employment_details = employment_details
            employee.termination_details = termination_details
            employee.save()

            return redirect("employees-list")
        else:
            print("Hubo un error")
            print(employee_form.errors)
            print(personal_info_form.errors)
            print(contact_info_form.errors)
            print(emergency_contact_form.errors)
            print(education_form.errors)
            print(employment_details_form.errors)
            print(termination_details_form.errors)
    else:
        print("Hubo un error")
        # Create empty forms for GET requests
        employee_form = EmployeeForm()
        personal_info_form = PersonalInformationForm()
        contact_info_form = ContactInformationForm()
        emergency_contact_form = EmergencyContactForm()
        education_form = EducationForm()
        employment_details_form = EmploymentDetailsForm()
        termination_details_form = TerminationDetailsForm()

    return render(
        request,
        "employees/employee_form.html",
        {
            "employee_form": employee_form,
            "personal_info_form": personal_info_form,
            "contact_info_form": contact_info_form,
            "emergency_contact_form": emergency_contact_form,
            "education_form": education_form,
            "employment_details_form": employment_details_form,
            "termination_details_form": termination_details_form,
        },
    )
