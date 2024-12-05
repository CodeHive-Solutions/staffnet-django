from datetime import datetime, timedelta

from django import forms
from django.forms import modelformset_factory
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
        # fields = "__all__"

    def clean(self):
        personal_info = PersonalInformationForm(self.data)
        if not personal_info.is_valid():
            for field, errors in personal_info.errors.items():
                for error in errors:
                    print(f"Error in {field}: {error}")
                    self.add_error(field, error)
        cleaned_data = super().clean()
        # print(self.emergency_contact.cleaned_data)
        termination_details = cleaned_data.get("termination_details")
        status = cleaned_data.get("status")

        if termination_details and status:
            raise forms.ValidationError(
                "An active employee cannot have termination details."
            )
        return cleaned_data

    def save(self, commit=True):
        print("Saving employee")
        super().save(commit=commit)
        # personal_info = self.personal_info.save(commit=False)
        # contact_info = self.contact_info.save(commit=False)
        # emergency_contact = self.emergency_contact.save(commit=False)
        # education = self.education.save(commit=False)
        # employment_details = self.employment_details.save(commit=False)
        # termination_details = self.termination_details.save(commit=False)

        # employee = super().save(commit=False)

        # personal_info.save()
        # contact_info.save()
        # emergency_contact.save()
        # education.save()
        # employment_details.save()
        # termination_details.save()

        # employee.personal_info = personal_info
        # employee.contact_info = contact_info
        # employee.emergency_contact = emergency_contact
        # employee.education = education
        # employee.employment_details = employment_details
        # employee.termination_details = termination_details

        # if commit:
        #     employee.save()

        # return employee


EmployeeFormSet = modelformset_factory(
    Employee,
    fields=["status", "personal_info", "contact_info", "emergency_contact"],
    extra=1,
)
