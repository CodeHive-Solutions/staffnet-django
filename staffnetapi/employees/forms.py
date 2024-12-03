from datetime import datetime, timedelta

from django import forms
from django.forms.models import inlineformset_factory

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
        for _, field in self.fields.items():
            if field.label and field.label.endswith("s") and "Hijos" not in field.label:
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue el {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


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
        for _, field in self.fields.items():
            if (
                field.label
                and field.label.endswith("s")
                and field.label != "Usuario de Windows"
            ):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


class TerminationDetailsForm(forms.ModelForm):
    class Meta:
        model = TerminationDetails
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.label and field.label.endswith("s"):
                placeholder = f"Agregue sus {str(field.label).lower()}"
            else:
                placeholder = f"Agregue su {str(field.label).lower()}"
            field.widget.attrs["placeholder"] = placeholder


class EmployeeForm(forms.ModelForm):
    personal_info = PersonalInformationForm()
    contact_info = ContactInformationForm()
    emergency_contact = EmergencyContactForm()
    education = EducationForm()
    employment_details = EmploymentDetailsForm()
    termination_details = TerminationDetailsForm()

    class Meta:
        model = Employee
        fields = ["status"]

    def clean(self):
        cleaned_data = super().clean()
        termination_details = cleaned_data.get("termination_details")
        status = cleaned_data.get("status")

        if termination_details and status:
            raise forms.ValidationError(
                "An active employee cannot have termination details."
            )
        return cleaned_data

    # def save(self, commit=True):
    #     # Save the parent model (Employee)
    #     employee = super().save(commit=False)
    #     if commit:
    #         employee.save()

    #     # Save related forms
    #     self.personal_info.instance = employee
    #     self.personal_info.save()

    #     self.contact_info.instance = employee
    #     self.contact_info.save()

    #     self.emergency_contact.instance = employee
    #     self.emergency_contact.save()

    #     self.education.instance = employee
    #     self.education.save()

    #     self.employment_details.instance = employee
    #     self.employment_details.save()

    #     return employee

    # def is_valid(self):
    #     # Check if the main form and all sub-forms are valid
    #     return super().is_valid() and all(
    #         form.is_valid()
    #         for form in [
    #             self.personal_info,
    #             self.contact_info,
    #             self.emergency_contact,
    #             self.education,
    #             self.employment_details,
    #             self.termination_details,
    #         ]
    #     )

    # def full_clean(self) -> None:
    #     super().full_clean()
    #     if not self.personal_info.is_valid():
    #         self.errors.update(
    #             {f"personal_info__{k}": v for k, v in self.personal_info.errors.items()}
    #         )
    #     if not self.contact_info.is_valid():
    #         self.errors.update(
    #             {f"contact_info__{k}": v for k, v in self.contact_info.errors.items()}
    #         )
    #     if not self.emergency_contact.is_valid():
    #         self.errors.update(
    #             {
    #                 f"emergency_contact__{k}": v
    #                 for k, v in self.emergency_contact.errors.items()
    #             }
    #         )
    #     if not self.education.is_valid():
    #         self.errors.update(
    #             {f"education__{k}": v for k, v in self.education.errors.items()}
    #         )
    #     if not self.employment_details.is_valid():
    #         self.errors.update(
    #             {
    #                 f"employment_details__{k}": v
    #                 for k, v in self.employment_details.errors.items()
    #             }
    #         )
    #     if not self.termination_details.is_valid():
    #         self.errors.update(
    #             {
    #                 f"termination_details__{k}": v
    #                 for k, v in self.termination_details.errors.items()
    #             }
    #         )
    #     print("Full clean")
    #     print(self.data)
    #     print("CLEANED DATA")
    #     print(self.cleaned_data)
    #     print("errors", self.errors)

    # def save(self, commit=True):
    #     # Save the main Employee model first
    #     employee = super().save(commit=False)

    #     personal_info = self.personal_info.save(commit=False)
    #     personal_info.employee = employee

    #     contact_info = self.contact_info.save(commit=False)
    #     contact_info.employee = employee

    #     emergency_contact = self.emergency_contact.save(commit=False)
    #     emergency_contact.employee = employee

    #     education = self.education.save(commit=False)
    #     education.employee = employee

    #     employment_details = self.employment_details.save(commit=False)
    #     employment_details.employee = employee

    #     termination_details = self.termination_details.save(commit=False)
    #     termination_details.employee = employee

    #     if commit:
    #         employee.save()
    #         personal_info.save()
    #         contact_info.save()
    #         emergency_contact.save()
    #         education.save()
    #         employment_details.save()
    #         termination_details.save()

    #     return employee
