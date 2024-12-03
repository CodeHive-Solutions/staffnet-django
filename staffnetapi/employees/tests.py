import os

import ldap  # type: ignore
from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from administration.models import *
from employees.forms import EmployeeForm
from employees.models import (
    ContactInformation,
    Education,
    EmergencyContact,
    Employee,
    EmploymentDetails,
    PersonalInformation,
    TerminationDetails,
)


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
        locality = Locality.objects.create(name="Test Locality")
        bank = Bank.objects.create(name="Test Bank")
        health_provider = HealthProvider.objects.create(name="Test Health Provider")
        pension_fund = PensionFund.objects.create(name="Test Pension Fund")
        compensation_fund = CompensationFund.objects.create(
            name="Test Compensation Fund"
        )
        saving_fund = SavingFund.objects.create(name="Test Savings Fund")
        headquarter = Headquarter.objects.create(name="Test Headquarter")
        job_title = JobTitle.objects.create(name="Test Job Title")
        management = Management.objects.create(name="Test Management")
        campaign = Campaign.objects.create(name="Test Campaign")

        self.personal_info = {
            "identification": 123456789,
            "expedition_place": "Bogotá",
            "birth_date": "1990-01-01",
            "last_name": "Doe",
            "first_name": "John",
            "document_type": "CC",
            "expedition_date": "2020-01-01",
            "gender": "M",
            "rh": "O+",
            "civil_status": "S",
            "sons": 0,
            "responsible_persons": 0,
            "stratum": 3,
            "shirt_size": "M",
            "pant_size": "32",
            "shoe_size": 9,
        }
        self.personal_info_input = {
            "personal_info__" + key: value for key, value in self.personal_info.items()
        }
        personal_info = PersonalInformation.objects.create(**self.personal_info)
        self.contact_info = {
            "address": "Calle 123",
            "neighborhood": "Barrio 123",
            "locality": locality,
            "fixed_phone": "12345678",
            "cell_phone": "1234567890",
            "email": settings.DEFAULT_FROM_EMAIL,
            "corporate_email": "test@test.com",
        }
        self.contact_info_input = {
            "contact_info__" + key: value for key, value in self.contact_info.items()
        }
        contact_info = ContactInformation.objects.create(**self.contact_info)
        self.emergency_contact = {
            "name": "Jane Doe",
            "relationship": "Mother",
            "phone": "1234567890",
        }
        self.emergency_contact_input = {
            "emergency_contact__" + key: value
            for key, value in self.emergency_contact.items()
        }
        emergency_contact = EmergencyContact.objects.create(**self.emergency_contact)
        self.education = {
            "education_level": "Professional",
            "title": "Engineer",
            "ongoing_studies": False,
        }
        self.education_input = {
            "education__" + key: value for key, value in self.education.items()
        }
        education = Education.objects.create(**self.education)
        self.employment_details = {
            "affiliation_date": "2021-01-01",
            "entry_date": "2021-01-01",
            "salary": 1000000,
            "transportation_allowance": 100000,
            "remote_work": True,
            "remote_work_application_date": "2021-01-01",
            "payroll_account": "123456789",
            "bank": bank,
            "health_provider": health_provider,
            "pension_fund": pension_fund,
            "compensation_fund": compensation_fund,
            "saving_fund": saving_fund,
            "headquarter": headquarter,
            "job_title": job_title,
            "appointment_date": "2021-01-01",
            "management": management,
            "campaign": campaign,
            "business_area": "Development",
            "contract_type": "Indefinite",
            "windows_user": "test.test",
        }
        self.employment_details_input = {
            "employment_details__" + key: value
            for key, value in self.employment_details.items()
        }
        employment_details = EmploymentDetails.objects.create(**self.employment_details)
        self.termination_details = {
            "termination_date": "2021-01-01",
            "termination_type": "Voluntary",
            "termination_reason": "Personal",
            "rehire_eligibility": False,
        }
        self.employee_data = {
            "personal_info": personal_info,
            "contact_info": contact_info,
            "emergency_contact": emergency_contact,
            "education": education,
            "employment_details": employment_details,
            "status": 1,
        }
        self.employee_data_input = {
             **self.personal_info_input,
            **self.contact_info_input,
            **self.emergency_contact_input,
            **self.education_input,
            **self.employment_details_input,
        }

    def test_form_data(self):
        """Tests that the form data is correct."""
        employee_form = EmployeeForm(data=self.employee_data)
        self.assertTrue(employee_form.is_valid(), employee_form.errors)

    # def create_employee(self):
    #     """Creates an employee."""
    #     personal_info = PersonalInformation.objects.create(**self.personal_info)
    #     contact_info = ContactInformation.objects.create(**self.contact_info)
    #     emergency_contact = EmergencyContact.objects.create(**self.emergency_contact)
    #     education = Education.objects.create(**self.education)
    #     employment_details = EmploymentDetails.objects.create(**self.employment_details)
    #     termination_details = TerminationDetails.objects.create(
    #         **self.termination_details
    #     )
    #     employee = Employee(
    #         personal_info=personal_info,
    #         contact_info=contact_info,
    #         emergency_contact=emergency_contact,
    #         education=education,
    #         employment_details=employment_details,
    #         termination_details=termination_details,
    #         status=1,
    #     )
    #     employee.full_clean()
    #     employee.save()
    #     return employee

    # def test_employee_str(self):
    #     """Tests that the employee string representation is correct."""
    #     employee = self.create_employee()
    #     self.assertEqual(str(employee), "John Doe (123456789)")

    # def test_employee_creation(self):
    #     """Tests that an employee is created correctly."""
    #     self.assertEqual(self.client.post(reverse("employee-create"), data=self.employee_data), 200)
    #     employee = Employee.objects.get(personal_info__identification=123456789)
    #     self.assertEqual(employee.personal_first_name, "JOHN")
    #     self.assertEqual(employee.personal_last_name, "DOE")
    #     self.assertEqual(employee.personal_identification, 123456789)
    #     self.assertEqual(employee.contact_email, self.contact_info["email"].upper())
    #     self.assertEqual(
    #         employee.contact_corporate_email,
    #         self.contact_info["corporate_email"].upper(),
    #     )
    #     self.assertEqual(employee.status, 1)
    #     # Personal Information Check
    #     self.assertFalse(employee.personal_info.photo)
    #     self.assertEqual(employee.personal_info.identification, 123456789)
    #     self.assertEqual(employee.personal_info.last_name, "DOE")
    #     self.assertEqual(employee.personal_info.first_name, "JOHN")
    #     self.assertEqual(employee.personal_info.document_type, "CC")
    #     self.assertEqual(employee.personal_info.birth_date, "1990-01-01")
    #     self.assertEqual(employee.personal_info.expedition_place, "BOGOTÁ")
    #     self.assertEqual(employee.personal_info.expedition_date, "2020-01-01")
    #     self.assertEqual(employee.personal_info.gender, "M")
    #     self.assertEqual(employee.personal_info.rh, "O+")
    #     self.assertEqual(employee.personal_info.civil_status, "S")
    #     self.assertEqual(employee.personal_info.sons, 0)
    #     self.assertEqual(employee.personal_info.responsible_persons, 0)
    #     self.assertEqual(employee.personal_info.stratum, 3)
    #     self.assertEqual(employee.personal_info.shirt_size, "M")
    #     self.assertEqual(employee.personal_info.pant_size, "32")
    #     self.assertEqual(employee.personal_info.shoe_size, 9)
    #     # Contact Information Check
    #     self.assertEqual(employee.contact_info.address, "CALLE 123")
    #     self.assertEqual(employee.contact_info.neighborhood, "BARRIO 123")
    #     self.assertEqual(employee.contact_info.locality, self.contact_info["locality"])
    #     self.assertEqual(employee.contact_info.fixed_phone, "12345678")
    #     self.assertEqual(employee.contact_info.cell_phone, "1234567890")
    #     self.assertEqual(
    #         employee.contact_info.email, self.contact_info["email"].upper()
    #     )
    #     self.assertEqual(
    #         employee.contact_info.corporate_email,
    #         self.contact_info["corporate_email"].upper(),
    #     )
    #     # Emergency Contact Check
    #     self.assertEqual(employee.emergency_contact.name, "JANE DOE")
    #     self.assertEqual(employee.emergency_contact.relationship, "MOTHER")
    #     self.assertEqual(employee.emergency_contact.phone, "1234567890")
    #     # Education Check
    #     self.assertEqual(employee.education.education_level, "PROFESSIONAL")
    #     self.assertEqual(employee.education.title, "ENGINEER")
    #     self.assertFalse(employee.education.ongoing_studies)
    #     # Employment Details Check
    #     self.assertEqual(employee.employment_details.affiliation_date, "2021-01-01")
    #     self.assertEqual(employee.employment_details.entry_date, "2021-01-01")
    #     self.assertEqual(employee.employment_details.salary, 1000000)
    #     self.assertEqual(employee.employment_details.transportation_allowance, 100000)
    #     self.assertTrue(employee.employment_details.remote_work)
    #     self.assertEqual(
    #         employee.employment_details.remote_work_application_date, "2021-01-01"
    #     )
    #     self.assertEqual(employee.employment_details.payroll_account, "123456789")
    #     self.assertEqual(
    #         employee.employment_details.bank, self.employment_details["bank"]
    #     )
    #     self.assertEqual(
    #         employee.employment_details.health_provider,
    #         self.employment_details["health_provider"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.legacy_health_provider,
    #         self.employment_details["legacy_health_provider"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.pension_fund,
    #         self.employment_details["pension_fund"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.compensation_fund,
    #         self.employment_details["compensation_fund"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.saving_fund,
    #         self.employment_details["saving_fund"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.headquarter,
    #         self.employment_details["headquarter"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.job_title, self.employment_details["job_title"]
    #     )
    #     self.assertEqual(employee.employment_details.appointment_date, "2021-01-01")
    #     self.assertEqual(
    #         employee.employment_details.legacy_appointment_date,
    #         self.employment_details["legacy_appointment_date"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.management,
    #         self.employment_details["management"],
    #     )
    #     self.assertEqual(
    #         employee.employment_details.campaign, self.employment_details["campaign"]
    #     )
    #     self.assertEqual(employee.employment_details.business_area, "DEVELOPMENT")
    #     self.assertEqual(employee.employment_details.contract_type, "INDEFINITE")
    #     self.assertEqual(employee.employment_details.windows_user, "TEST.TEST")
    #     # Termination Details Check
    #     self.assertEqual(employee.termination_details.termination_date, "2021-01-01")

    # # def test_create_all(self):
    # #     """Tests that all the employee fields are created."""
    # #     response = self.client.get(reverse("get_employees_from_db"))
    # #     self.assertEqual(response.status_code, 200)

    # # def test_create_no_remote_work(self):
    # #     """Tests that the employee is created without remote work."""
    # #     self.employee_data["remote_work"] = False
    # #     self.employee_data["remote_work_application_date"] = "2021-01-01"
    # #     with self.assertRaises(ValidationError):
    # #         employee = Employee.objects.create(**self.employee_data)
    # #         employee.full_clean()
