from datetime import datetime, timedelta

from django import forms

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
    # Add sub-forms as embedded forms
    personal_info = PersonalInformationForm(prefix="personal_info")
    contact_info = ContactInformationForm(prefix="contact_info")
    emergency_contact = EmergencyContactForm(prefix="emergency_contact")
    education = EducationForm(prefix="education")
    employment_details = EmploymentDetailsForm(prefix="employment_details")
    termination_details = TerminationDetailsForm(prefix="termination_details")

    class Meta:
        model = Employee
        fields = ["status"]  # Main Employee fields

    def save(self, commit=True):
        # Save the main Employee model first
        employee = super().save(commit=False)

        # Save related models (using their respective forms)
        personal_info = self.cleaned_data["personal_info"]
        contact_info = self.cleaned_data["contact_info"]
        emergency_contact = self.cleaned_data["emergency_contact"]
        education = self.cleaned_data["education"]
        employment_details = self.cleaned_data["employment_details"]
        termination_details = self.cleaned_data["termination_details"]

        if commit:
            employee.save()
            # Save related models with `OneToOneField` links
            personal_info.employee = employee
            personal_info.save()

            contact_info.employee = employee
            contact_info.save()

            emergency_contact.employee = employee
            emergency_contact.save()

            education.employee = employee
            education.save()

            employment_details.employee = employee
            employment_details.save()

            termination_details.employee = employee
            termination_details.save()

        return employee
