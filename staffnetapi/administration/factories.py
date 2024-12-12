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


class BankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bank

    name = factory.Faker("company")


class HealthProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HealthProvider

    name = factory.Faker("company")


class PensionFundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PensionFund

    name = factory.Faker("company")


class CompensationFundFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompensationFund

    name = factory.Faker("company")


class SavingFundFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = SavingFund

    name = factory.Faker("company")


class HeadquarterFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Headquarter

    name = factory.Faker("company")


class JobTitleFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = JobTitle

    name = factory.Faker("job")


class ManagementFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Management

    name = factory.Faker("company")


class CampaignFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Campaign

    name = factory.Faker("company")
