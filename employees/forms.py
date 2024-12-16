from datetime import datetime, timedelta

from django import forms
from django.conf import settings

from administration.models import (
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
from employees.factories import (
    ContactInformationFactory,
    EducationFactory,
    EmergencyContactFactory,
    EmploymentDetailsFactory,
    PersonalInformationFactory,
    TerminationDetailsFactory,
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

calendar_attrs = {
    "datepicker": "",
    "datepicker-autohide": "",
    "class": "cursor-pointer",
    # Set the minimum date to 100 years ago
    "datepicker-min-date": (datetime.now() - timedelta(days=365 * 100)).strftime(
        "%d-%m-%Y"
    ),
    "datepicker-format": "dd/mm/yyyy",
    "style": "background: url('data:image/svg+xml,%3Csvg xmlns%3D%27http%3A//www.w3.org/2000/svg%27 fill%3D%27%236b7280%27 viewBox%3D%270 0 20 20%27%3E%3Cpath d%3D%27M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z%27/%3E%3C/svg%3E') no-repeat left 0.75rem center; background-size: 1rem;",
}

calendar_today_max_attrs = {
    # Extend `calendar_attrs` with today's date as the maximum date
    **calendar_attrs,
    "datepicker-max-date": datetime.now().strftime("%d-%m-%Y"),
}

DEBUG = settings.DEBUG


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = "__all__"
        widgets = {
            "expedition_date": forms.DateInput(attrs={**calendar_today_max_attrs}),
            "birth_date": forms.DateInput(attrs={**calendar_today_max_attrs}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        personal_information = PersonalInformationFactory.build()
        for name, field in self.fields.items():
            if field.label and field.label.endswith("s") and "Hijos" not in field.label:
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            if isinstance(field.widget, forms.TextInput) or isinstance(
                field.widget, forms.NumberInput
            ):
                field.widget.attrs["autocomplete"] = "off"
                field.widget.attrs["autofill"] = "off"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(personal_information, name)


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if DEBUG:
            locality = Locality.objects.first()
            contact_information = ContactInformationFactory.build(locality=locality)

        for name, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(contact_information, name)


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        emergency_contact = EmergencyContactFactory.build()
        for name, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue el {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(emergency_contact, name)


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        education = EducationFactory.build()
        for name, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(education, name)


class EmploymentDetailsForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        fields = "__all__"
        widgets = {
            # Format salary to COP
            "salary": forms.TextInput(),
            "transportation_allowance": forms.TextInput(),
            "affiliation_date": forms.DateInput(attrs={**calendar_attrs}),
            "entry_date": forms.DateInput(attrs={**calendar_attrs}),
            "remote_work_application_date": forms.DateInput(attrs={**calendar_attrs}),
            "appointment_date": forms.DateInput(attrs={**calendar_attrs}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if DEBUG:
            bank = Bank.objects.first()
            campaign = Campaign.objects.first()
            compensation_fund = CompensationFund.objects.first()
            health_provider = HealthProvider.objects.first()
            headquarter = Headquarter.objects.first()
            job_title = JobTitle.objects.first()
            management = Management.objects.first()
            pension_fund = PensionFund.objects.first()
            saving_fund = SavingFund.objects.first()
            employment_details = EmploymentDetailsFactory.build(
                bank=bank,
                campaign=campaign,
                compensation_fund=compensation_fund,
                health_provider=health_provider,
                headquarter=headquarter,
                job_title=job_title,
                management=management,
                pension_fund=pension_fund,
                saving_fund=saving_fund,
            )
        for name, field in self.fields.items():
            if (
                field.label
                and field.label.endswith("s")
                and field.label != "Usuario de Windows"
            ):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(employment_details, name)


class TerminationDetailsForm(forms.ModelForm):
    class Meta:
        model = TerminationDetails
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        termination_details = TerminationDetailsFactory.build()
        for name, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder
            if DEBUG:
                self.fields[name].initial = getattr(termination_details, name)


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["status"]
