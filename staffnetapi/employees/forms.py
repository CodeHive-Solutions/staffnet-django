# employees/forms.py

from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        widgets = {
            'birth_date': AdminDateWidget(),  # Replace with your date field
        }