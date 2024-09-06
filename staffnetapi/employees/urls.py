# urls for the employees app.

from django.urls import path
from .views import home, ListEmployees, DetailEmployee, CreateEmployee

urlpatterns = [
    path("", home),
    path("list/", ListEmployees.as_view(), name="employee_list"),
    path("detail/<int:pk>/", DetailEmployee.as_view(), name="employee_detail"),
    path("create/", CreateEmployee.as_view(), name="employee_create"),
]
