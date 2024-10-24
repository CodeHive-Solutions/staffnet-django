import os
from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from administration.models import *
from employees.forms import EmployeeForm

from .models import Employee


def parse_date(date_str):
    """Parses a date string."""
    if not date_str:
        return None
    date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return date_obj.strftime("%Y-%m-%d")


def get_employees_from_db(request):
    """Gets the employees from the external API."""
    # First delete all records from the models
    Employee.objects.all().delete()
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
    # Set the cookie token
    cookie_token = "7ca6b0de-2d43-4ab9-967b-01ffdabbb4d8"
    # set the cookie
    request.COOKIES["StaffNet"] = cookie_token
    # Request the employees from the external API using the cookie token
    response = requests.post(
        "https://staffnet-api.cyc-bpo.com/search_employees",
        cookies=request.COOKIES,
    )
    employees = response.json()
    if employees.get("error"):
        return JsonResponse({"error": employees["error"]}, status=500)
    employees_batch = []
    # Save the employees to the database
    for employee_data in employees["info"]["data"]:

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
        employees_batch.append(
            Employee(
                identification=int(employee_data["cedula"]),
                last_name=employee_data["apellidos"],
                first_name=employee_data["nombres"],
                document_type=employee_data["tipo_documento"],
                birth_date=parse_date(employee_data["fecha_nacimiento"]),
                expedition_place=employee_data["lugar_expedicion"] or "No especificado",
                expedition_date=parse_date(
                    # ! Delete after testing
                    employee_data["fecha_expedicion"]
                    or "Mon, 01 Jan 1900 00:00:00 GMT"
                ),
                gender="M" if employee_data["genero"] == "MASCULINO" else "F",
                rh=employee_data["rh"] or "O+",
                civil_status=employee_data["estado_civil"],
                sons=employee_data["hijos"] or 0,
                responsible_persons=employee_data["personas_a_cargo"] or 0,
                stratum=employee_data["estrato"] or 2,
                fixed_phone=employee_data["tel_fijo"],
                cell_phone=employee_data["celular"] or 0,
                email=employee_data["correo"],
                corporate_email=employee_data["correo_corporativo"],
                address=employee_data["direccion"] or "No especificada",
                neighborhood=employee_data["barrio"] or "No especificado",
                locality=Locality.objects.get_or_create(
                    name=employee_data["localidad"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                emergency_contact=employee_data["contacto_emergencia"]
                or "No especificado",
                emergency_relationship=employee_data["parentesco"] or "OTRO",
                emergency_phone=employee_data["tel_contacto"] or "No especificado",
                education_level=employee_data["nivel_escolaridad"],
                title=employee_data["profesion"],
                ongoing_studies=bool(employee_data["estudios_en_curso"]),
                affiliation_date=parse_date(
                    employee_data["fecha_afiliacion_eps"]
                    or employee_data["fecha_ingreso"]
                ),
                health_provider=HealthProvider.objects.get_or_create(
                    name=employee_data["eps"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                legacy_health_provider=employee_data["cambio_eps_legado"],
                pension_fund=PensionFund.objects.get_or_create(
                    name=employee_data["pension"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                compensation_fund=CompensationFund.objects.get_or_create(
                    name=employee_data["caja_compensacion"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                saving_fund=SavingFund.objects.get_or_create(
                    name=employee_data["cesantias"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                payroll_account=employee_data["cuenta_nomina"] or 0,
                bank=Bank.objects.get_or_create(
                    name=employee_data["banco"] or "BANCO CAJA SOCIAL"
                )[
                    0
                ],  # Fetching from database
                headquarter=Headquarter.objects.get_or_create(
                    name=employee_data["sede"] or "No especificada"
                )[
                    0
                ],  # Fetching from database
                job_title=JobTitle.objects.get_or_create(name=employee_data["cargo"])[
                    0
                ],  # Fetching from database
                appointment_date=(
                    parse_date(employee_data["fecha_nombramiento"])
                    if employee_data["fecha_nombramiento"]
                    else None
                ),
                legacy_appointment_date=(employee_data["fecha_nombramiento_legado"]),
                management=Management.objects.get_or_create(
                    name=employee_data["gerencia"] or "BANCO AGRARIO"
                )[
                    0
                ],  # Fetching from database
                campaign=Campaign.objects.get_or_create(
                    name=employee_data["campana_general"]
                )[
                    0
                ],  # Fetching from database
                business_area=employee_data["area_negocio"],
                contract_type=employee_data["tipo_contrato"] or "OBRA O LABOR",
                entry_date=parse_date(employee_data["fecha_ingreso"]),
                salary=employee_data["salario"],
                transportation_allowance=employee_data["subsidio_transporte"] or 0,
                remote_work=bool(employee_data["aplica_teletrabajo"]),
                remote_work_application_date=(
                    parse_date(employee_data["fecha_aplica_teletrabajo"])
                    if employee_data["fecha_aplica_teletrabajo"]
                    else None
                ),
                shirt_size=employee_data.get("talla_camisa"),
                pant_size=employee_data.get("talla_pantalon"),
                shoe_size=employee_data.get("talla_zapatos"),
                windows_user=employee_data.get("usuario_windows"),
                memo_1=employee_data.get("memorando_1"),
                memo_2=employee_data.get("memorando_2"),
                memo_3=employee_data.get("memorando_3"),
                photo=(
                    f"employees/photos/{employee_data['cedula']}.webp"
                    if photo_exists
                    else None
                ),
            )
        )
    print(employees_batch)
    Employee.objects.bulk_create(employees_batch)
    return JsonResponse({"message": "Employees saved to the database."})


class EmployeeListView(ListView):
    """Employee list view."""

    model = Employee
    template_name = "employees/employees-list.html"
    context_object_name = "employees"
    paginate_by = 11

    def get_queryset(self):
        """Get the queryset."""
        queryset = Employee.objects.only(
            "first_name", "last_name", "identification", "job_title", "status"
        ).order_by("first_name", "last_name")
        query = self.request.GET.get("q")
        if query:
            # Filter the queryset based on the search query
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(identification__icontains=query)
                | Q(job_title__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """Get the context data."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Employees"
        return context


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
        print(context["fields"])
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
