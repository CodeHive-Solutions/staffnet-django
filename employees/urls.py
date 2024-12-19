# urls for the employees app.

from django.urls import path

from .views import EmployeeDetailView  # create_employee,
from .views import (
    CreateEmployeeView,
    EmployeeListView,
    UpdateEmployeeView,
    get_employees_from_db,
)

urlpatterns = [
    path("get_employees_from_db/", get_employees_from_db, name="get_employees_from_db"),
    path("list/", EmployeeListView.as_view(), name="employees-list"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employees-detail"),
    path("create/", CreateEmployeeView.as_view(), name="employee-create"),
    path("<int:pk>/update/", UpdateEmployeeView.as_view(), name="employee-update"),
]
