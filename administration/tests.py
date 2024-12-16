# from django.test import TestCase

# from .factories import (
#     BankFactory,
#     CampaignFactory,
#     CompensationFundFactory,
#     HeadquarterFactory,
#     HealthProviderFactory,
#     JobTitleFactory,
#     LocalityFactory,
#     ManagementFactory,
#     PensionFundFactory,
#     SavingFundFactory,
# )
# from .models import (
#     Bank,
#     Campaign,
#     CompensationFund,
#     Headquarter,
#     HealthProvider,
#     JobTitle,
#     Locality,
#     Management,
#     PensionFund,
#     SavingFund,
# )


# # Create your tests here.
# class FactoryTest(TestCase):
#     def test_locality_factory(self):
#         locality = LocalityFactory()
#         self.assertTrue(isinstance(locality, Locality))

#     def test_bank_factory(self):
#         bank = BankFactory()
#         self.assertTrue(isinstance(bank, Bank))

#     def test_health_provider_factory(self):
#         health_provider = HealthProviderFactory()
#         self.assertTrue(isinstance(health_provider, HealthProvider))

#     def test_pension_fund_factory(self):
#         pension_fund = PensionFundFactory()
#         self.assertTrue(isinstance(pension_fund, PensionFund))

#     def test_compensation_fund_factory(self):
#         compensation_fund = CompensationFundFactory()
#         self.assertTrue(isinstance(compensation_fund, CompensationFund))

#     def test_saving_fund_factory(self):
#         saving_fund = SavingFundFactory()
#         self.assertTrue(isinstance(saving_fund, SavingFund))

#     def test_headquarter_factory(self):
#         headquarter = HeadquarterFactory()
#         self.assertTrue(isinstance(headquarter, Headquarter))

#     def test_job_title_factory(self):
#         job_title = JobTitleFactory()
#         self.assertTrue(isinstance(job_title, JobTitle))

#     def test_management_factory(self):
#         management = ManagementFactory()
#         self.assertTrue(isinstance(management, Management))

#     def test_campaign_factory(self):
#         campaign = CampaignFactory()
#         self.assertTrue(isinstance(campaign, Campaign))
