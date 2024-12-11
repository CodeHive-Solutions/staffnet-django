from django.conf import settings
from django.test import Client, TestCase

from administration.models import *
from employees.forms import EmployeeForm
from employees.models import (ContactInformation, Education, EmergencyContact,
                              Employee, EmploymentDetails, PersonalInformation,
                              TerminationDetails)

from .factories import ContactInformationFactory, PersonalInformationFactory


class EmployeeModelTest(TestCase):
    """Tests the Employee model and his related models."""

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


class FactoryTest(TestCase):
    """Tests the factories of the employees app."""

    def test_contact_information_factory(self):
        """Tests the ContactInformation factory."""
        contact_information = ContactInformationFactory()
        self.assertTrue(isinstance(contact_information, ContactInformation))

    def test_personal_information_factory(self):
        """Tests the PersonalInformation factory."""
        personal_information = PersonalInformationFactory()
        self.assertTrue(isinstance(personal_information, PersonalInformation))
        print(personal_information.__dict__)