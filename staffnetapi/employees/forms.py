from django import forms

from .models import Employee  # Import your Employee model


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee  # The model the form is based on
        fields = "__all__"
