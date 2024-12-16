# factories.py
import factory
from faker import Faker

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

from .choices import (
    BusinessArea,
    CivilStatus,
    ContractType,
    DocumentType,
    EducationLevel,
    Gender,
    Relationship,
    Rh,
    ShirtSize,
    TerminationReason,
    TerminationType,
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
from .utilities import get_choices_values


# Set faker to Spanish
faker = Faker("es_CO")


class PersonalInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PersonalInformation

    photo = factory.django.ImageField()
    identification = factory.Faker("numerify", text="1#########")
    last_name = factory.LazyFunction(lambda: "Test_" + faker.last_name())
    first_name = factory.LazyFunction(lambda: "Test_" + faker.first_name())
    # last_name = factory.Faker("last_name")
    # first_name = factory.Faker("first_name")
    document_type = factory.Faker("random_element", elements=["CC", "CE", "TI"])
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=65)
    expedition_place = factory.Faker("city")
    expedition_date = factory.Faker("date_this_century", before_today=True)
    gender = factory.Faker(
        "random_element", elements=get_choices_values(Gender.choices)
    )
    rh = factory.Faker(
        "random_element",
        elements=get_choices_values(Rh.choices),
    )
    civil_status = factory.Faker(
        "random_element",
        elements=get_choices_values(CivilStatus.choices),
    )
    sons = factory.Faker("random_int", min=0, max=20)
    responsible_persons = factory.Faker("random_int", min=0, max=20)
    stratum = factory.Faker("random_int", min=1, max=6)
    shirt_size = factory.Faker(
        "random_element",
        elements=get_choices_values(ShirtSize.choices),
    )
    pant_size = factory.Faker("random_int", min=6, max=44)
    shoe_size = factory.Faker("random_int", min=20, max=45)


class ContactInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactInformation

    address = factory.Faker("address")
    neighborhood = factory.Faker("secondary_address")
    locality = factory.SubFactory(LocalityFactory)
    fixed_phone = factory.Faker("numerify", text="#######")
    cell_phone = factory.Faker("numerify", text="3#########")
    email = factory.Faker("email")
    corporate_email = factory.Faker("email")


class EmergencyContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmergencyContact

    name = factory.Faker("name")
    relationship = factory.Faker(
        "random_element",
        elements=get_choices_values(Relationship.choices),
    )
    phone = factory.Faker("numerify", text="1#########")


class EducationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Education

    education_level = factory.Faker(
        "random_element",
        elements=get_choices_values(EducationLevel.choices),
    )
    title = factory.Faker("job")
    ongoing_studies = factory.Faker("boolean")


class EmploymentDetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmploymentDetails

    affiliation_date = factory.Faker("date_this_century", before_today=True)
    entry_date = factory.Faker("date_this_century", before_today=True)
    salary = factory.Faker("random_int", min=1000000, max=90000000)
    transportation_allowance = factory.Faker("random_int", min=0, max=1000000)
    payroll_account = factory.Faker("numerify", text="#########")
    bank = factory.SubFactory(BankFactory)
    health_provider = factory.SubFactory(HealthProviderFactory)
    pension_fund = factory.SubFactory(PensionFundFactory)
    compensation_fund = factory.SubFactory(CompensationFundFactory)
    saving_fund = factory.SubFactory(SavingFundFactory)
    headquarter = factory.SubFactory(HeadquarterFactory)
    job_title = factory.SubFactory(JobTitleFactory)
    appointment_date = factory.Faker("date_this_century", before_today=True)
    management = factory.SubFactory(ManagementFactory)
    campaign = factory.SubFactory(CampaignFactory)
    business_area = factory.Faker(
        "random_element",
        elements=get_choices_values(BusinessArea.choices),
    )
    contract_type = factory.Faker(
        "random_element",
        elements=get_choices_values(ContractType.choices),
    )
    windows_user = factory.Faker("user_name")
    remote_work = factory.Faker("boolean")
    remote_work_application_date = factory.Maybe(
        "remote_work",
        yes_declaration=factory.Faker("date_this_century", before_today=True),  # type: ignore
        no_declaration=None,  # type: ignore
    )


class TerminationDetailsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TerminationDetails

    termination_date = factory.Faker("date_this_century", before_today=True)
    termination_type = factory.Faker(
        "random_element",
        elements=get_choices_values(TerminationType.choices),
    )
    termination_reason = factory.Faker(
        "random_element",
        elements=get_choices_values(TerminationReason.choices),
    )
    rehire_eligibility = factory.Faker("boolean")


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    personal_info = factory.SubFactory(PersonalInformationFactory)
    contact_info = factory.SubFactory(ContactInformationFactory)
    emergency_contact = factory.SubFactory(EmergencyContactFactory)
    education = factory.SubFactory(EducationFactory)
    employment_details = factory.SubFactory(EmploymentDetailsFactory)
    termination_details = factory.SubFactory(TerminationDetailsFactory)
    status = factory.Faker("boolean")
