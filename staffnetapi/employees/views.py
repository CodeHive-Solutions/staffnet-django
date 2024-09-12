import requests
from datetime import datetime
from django.http import JsonResponse
from administration.models import *
from .models import Employee


def parse_date(date_str):
    """Parses a date string."""
    if not date_str:
        return None
    date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    return date_obj.strftime("%Y-%m-%d")


def get_employees_from_db(request):
    """Gets the employees from the external API."""
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
    # Save the employees to the database
    for employee_data in employees["info"]["data"]:
        # Set some columns in None if they are empty
        for key in employee_data:
            key = key.lower()
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
        print(employee_data)
        Employee.objects.create(
            identification=int(employee_data["cedula"]),
            last_name=employee_data["apellidos"],
            first_name=employee_data["nombres"],
            document_type=employee_data["tipo_documento"],
            birth_date=parse_date(employee_data["fecha_nacimiento"]),
            expedition_place=employee_data["lugar_expedicion"] or "No especificado",
            expedition_date=parse_date(
                # ! Delete after testing
                employee_data["fecha_expedicion"]
                or "Fri, 04 Aug 2023 00:00:00 GMT"
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
            emergency_contact=employee_data["contacto_emergencia"] or "No especificado",
            emergency_relationship=employee_data["parentesco"] or "OTRO",
            emergency_phone=employee_data["tel_contacto"] or "No especificado",
            education_level=employee_data["nivel_escolaridad"],
            title=employee_data["profesion"],
            ongoing_studies=bool(employee_data["estudios_en_curso"]),
            affiliation_date=parse_date(
                employee_data["fecha_afiliacion_eps"] or employee_data["fecha_ingreso"]
            ),
            health_provider=HealthProvider.objects.get_or_create(
                name=employee_data["eps"] or "No especificada"
            )[
                0
            ],  # Fetching from database
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
            management=Management.objects.get_or_create(name=employee_data["gerencia"])[
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
        )
    return JsonResponse({"message": "Employees saved to the database."})
