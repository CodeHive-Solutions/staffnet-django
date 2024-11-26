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


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = "__all__"


class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = "__all__"


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = "__all__"


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = "__all__"


class EmploymentDetailsForm(forms.ModelForm):
    class Meta:
        model = EmploymentDetails
        fields = "__all__"


class TerminationDetailsForm(forms.ModelForm):
    class Meta:
        model = TerminationDetails
        fields = "__all__"


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
