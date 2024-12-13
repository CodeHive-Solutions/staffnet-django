import factory
from django.test import TestCase
from django.urls import reverse

from administration.factories import (
    BankFactory,
    CampaignFactory,
    CompensationFundFactory,
    HeadquarterFactory,
    HealthProviderFactory,
    JobTitleFactory,
    LocalityFactory,
    ManagementFactory,
    PensionFundFactory,
    SavingFundFactory,
)
from employees.models import (
    ContactInformation,
    Education,
    EmergencyContact,
    Employee,
    EmploymentDetails,
    PersonalInformation,
    TerminationDetails,
)

from .factories import (
    ContactInformationFactory,
    EducationFactory,
    EmergencyContactFactory,
    EmployeeFactory,
    EmploymentDetailsFactory,
    PersonalInformationFactory,
    TerminationDetailsFactory,
)


class EmployeeModelTest(TestCase):
    """Tests the Employee model and his related models."""

    def setUp(self):
        """Sets up the test client."""
        self.personal_info = factory.build(
            dict, FACTORY_CLASS=PersonalInformationFactory
        )
        self.contact_info = factory.build(
            dict, FACTORY_CLASS=ContactInformationFactory, locality=LocalityFactory().pk
        )
        self.emergency_contact = factory.build(
            dict, FACTORY_CLASS=EmergencyContactFactory
        )
        self.education = factory.build(dict, FACTORY_CLASS=EducationFactory)
        self.employment_details = factory.build(
            dict,
            FACTORY_CLASS=EmploymentDetailsFactory,
            bank=BankFactory().pk,
            health_provider=HealthProviderFactory().pk,
            pension_fund=PensionFundFactory().pk,
            compensation_fund=CompensationFundFactory().pk,
            saving_fund=SavingFundFactory().pk,
            headquarter=HeadquarterFactory().pk,
            job_title=JobTitleFactory().pk,
            management=ManagementFactory().pk,
            campaign=CampaignFactory().pk,
        )
        if not self.employment_details["remote_work"]:
            self.employment_details.pop("remote_work_application_date")
        self.termination_details = factory.build(
            dict, FACTORY_CLASS=TerminationDetailsFactory
        )
        self.employee = {
            **self.personal_info,
            **self.contact_info,
            **self.emergency_contact,
            **self.education,
            **self.employment_details,
            **self.termination_details,
        }

    def test_create_employee(self):
        """Tests the creation of an employee."""
        response = self.client.post(reverse("employee-create"), self.employee)
        self.assertEqual(response.status_code, 302, response.status_code)
        self.assertTrue(Employee.objects.exists())
        self.assertTrue(Employee.objects.first().status)  # type: ignore
        self.assertTrue(PersonalInformation.objects.exists())
        self.assertTrue(ContactInformation.objects.exists())
        self.assertTrue(EmergencyContact.objects.exists())
        self.assertTrue(Education.objects.exists())
        self.assertTrue(EmploymentDetails.objects.exists())
        self.assertTrue(TerminationDetails.objects.exists())


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

    def test_emergency_contact_factory(self):
        """Tests the EmergencyContact factory."""
        emergency_contact = EmergencyContactFactory()
        self.assertTrue(isinstance(emergency_contact, EmergencyContact))

    def test_education_factory(self):
        """Tests the Education factory."""
        education = EducationFactory()
        self.assertTrue(isinstance(education, Education))

    def test_employment_details_factory(self):
        """Tests the EmploymentDetails factory."""
        employment_details = EmploymentDetailsFactory()
        self.assertTrue(isinstance(employment_details, EmploymentDetails))

    def test_termination_details_factory(self):
        """Tests the TerminationDetails factory."""
        termination_details = TerminationDetailsFactory()
        self.assertTrue(isinstance(termination_details, TerminationDetails))

    def test_employee_factory(self):
        """Tests the Employee factory."""
        employee = EmployeeFactory()
        self.assertTrue(isinstance(employee, Employee))
