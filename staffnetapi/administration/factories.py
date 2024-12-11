import factory

from .models import (
    Bank,
    Campaign,
    CompensationFund,
    Headquarter,
    HealthProvider,
    JobTitle,
    Locality,
    Management,
    PensionFund,
    SavingFund,
)

factory.Faker._DEFAULT_LOCALE = "es_CO"


class LocalityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Locality

    name = factory.Faker("municipality")
