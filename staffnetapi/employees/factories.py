# factories.py
import factory

from administration.factories import LocalityFactory

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


class PersonalInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PersonalInformation

    photo = factory.django.ImageField()
    identification = factory.Faker("numerify", text="1#########")
    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
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
    pant_size = factory.Faker("numerify", text="##")
    shoe_size = factory.Faker("numerify", text="##")


class ContactInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactInformation

    address = factory.Faker("address")
    neighborhood = factory.Faker("secondary_address")
    locality = factory.SubFactory(LocalityFactory)
    fixed_phone = factory.Faker("numerify", text="#######")
    cell_phone = factory.Faker("numerify", text="##########")
    email = factory.Faker("email")
    corporate_email = factory.Faker("email")
