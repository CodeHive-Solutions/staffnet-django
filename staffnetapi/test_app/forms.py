from django import forms
from .models import User, Project, UserProject
from django.forms import modelformset_factory

class FormOne(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

class FormTwo(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'start_date']

# FormSet for UserProject to handle the relationship
UserProjectFormSet = modelformset_factory(UserProject, fields=['user', 'project'], extra=1)
