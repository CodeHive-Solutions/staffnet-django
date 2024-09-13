import os
import ldap  # type: ignore
from django.urls import reverse
from django.test import TestCase
from django.test import Client
from django.conf import settings
from django.core.exceptions import ValidationError
from employees.models import Employee
from administration.models import *


class LDAPAuthenticationTest(TestCase):
    """Tests the LDAP authentication."""

    databases = "__all__"

    def setUp(self):
        """Sets up the test client."""
        self.client = Client()

    def test_ldap_connection(self):
        """Tests that the connection to the LDAP server is successful."""
        ldap_server_uri = settings.AUTH_LDAP_SERVER_URI
        ldap_bind_dn = settings.AUTH_LDAP_BIND_DN
        ldap_bind_password = settings.AUTH_LDAP_BIND_PASSWORD
        conn = None
        try:
            conn = ldap.initialize(ldap_server_uri)
            conn.simple_bind_s(ldap_bind_dn, ldap_bind_password)
        except ldap.LDAPError as err:
            self.fail(f"Error: {err}")
        finally:
            if conn:
                conn.unbind_s()

    def test_login(self):
        """Tests that the user can login using LDAP."""
        ldap_server_uri = settings.AUTH_LDAP_SERVER_URI
        ldap_bind_dn = settings.AUTH_LDAP_BIND_DN
        ldap_bind_password = settings.AUTH_LDAP_BIND_PASSWORD
        username = "staffnet"
        password = os.environ["StaffNetLDAP"]
        conn = None
        try:
            conn = ldap.initialize(ldap_server_uri)
            conn.simple_bind_s(ldap_bind_dn, ldap_bind_password)
            search_filter = "(sAMAccountName={})".format(username)
            search_base = "dc=CYC-SERVICES,dc=COM,dc=CO"
            attributes = ["dn"]
            result_id = conn.search(
                search_base, ldap.SCOPE_SUBTREE, search_filter, attributes
            )
            _, result_data = conn.result(result_id, 0)
            self.assertTrue(result_data, "User entry not found.")
            if result_data:
                user_dn = result_data[0][0]
                logged = conn.simple_bind_s(user_dn, password)
                self.assertTrue(logged, "User authentication failed.")
        except ldap.LDAPError as err:
            self.fail("Error: %s" % err)
        finally:
            if conn:
                conn.unbind()


class EmployeeModelTest(TestCase):
    """Tests the Employee model."""

    databases = "__all__"

    def setUp(self):
        """Sets up the test client."""
        self.client = Client()

        self.employee_data = {
            "first_name": "John",
            "last_name": "Doe",
            "identification": 123456789,
            "birth_date": "1990-01-01",
            "expedition_place": "Bogotá",
            "expedition_date": "2010-01-01",
            "email": "test@gmail.com",
            "locality": Locality.objects.create(name="Bogotá"),
            "affiliation_date": "2021-01-01",
            "document_type": "CC",
            "job_title": JobTitle.objects.create(name="Software Developer"),
            "appointment_date": "2021-01-01",
            "gender": "M",
            "rh": "O+",
            "civil_status": "SOLTERO(A)",
            "stratum": "3",
            "cell_phone": "1234567890",
            "address": "Cra 1 # 1-1",
            "neighborhood": "Barrio",
            "emergency_contact": "Jane Doe",
            "emergency_relationship": "MADRE",
            "emergency_phone": "987654321",
            "education_level": "BACHILLER",
            "title": "Software Engineering",
            "business_area": "OPERATIVOS",
            "contract_type": "TERMINO INDEFINIDO",
            "management": Management.objects.create(name="Software Development"),
            "campaign": Campaign.objects.create(name="Software Development"),
            "health_provider": HealthProvider.objects.create(name="EPS Sura"),
            "pension_fund": PensionFund.objects.create(name="Colpensiones"),
            "compensation_fund": CompensationFund.objects.create(name="Compensar"),
            "saving_fund": SavingFund.objects.create(name="Fondo Nacional del Ahorro"),
            "payroll_account": "123456789",
            "bank": Bank.objects.create(name="Banco de Bogotá"),
            "headquarter": Headquarter.objects.create(name="Bogotá"),
            "entry_date": "2021-01-01",
            "salary": 1000000,
            "transportation_allowance": 100000,
            "remote_work": False,
            "remote_work_application_date": None,
            "shirt_size": 10,
            "pant_size": 10,
            "shoe_size": 30,
        }

    def test_employee_str(self):
        """Tests that the employee string representation is correct."""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(str(employee), "JOHN DOE - 123456789")

    def test_employee_save(self):
        """Tests that the employee info is saved in uppercase."""
        employee = Employee.objects.create(**self.employee_data)
        self.assertEqual(employee.first_name, "JOHN")
        self.assertEqual(employee.last_name, "DOE")
        self.assertEqual(employee.identification, 123456789)
        self.assertEqual(employee.expedition_place, "BOGOTÁ")
        self.assertEqual(employee.email, self.employee_data["email"].upper())

    def test_create_all(self):
        """Tests that all the employee fields are created."""
        response = self.client.get(reverse("get_employees_from_db"))
        self.assertEqual(response.status_code, 200)

    def test_create_no_remote_work(self):
        """Tests that the employee is created without remote work."""
        self.employee_data["remote_work"] = False
        self.employee_data["remote_work_application_date"] = "2021-01-01"
        with self.assertRaises(ValidationError):
            employee = Employee.objects.create(**self.employee_data)
            employee.full_clean()
