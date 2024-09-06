from django.shortcuts import render
from .models import Employee

# Create your views here.
from django.http import HttpResponse
from django.views import generic


def home(request):
    return HttpResponse("Hello, World!")


class ListEmployees(generic.ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10


class DetailEmployee(generic.DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"


class CreateEmployee(generic.CreateView):
    model = Employee
    template_name = "employees/employee_form.html"
    fields = "__all__"
