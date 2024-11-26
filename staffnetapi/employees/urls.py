# urls for the employees app.

from django.urls import path

from .views import (
    EmployeeDetailView,
    EmployeeListView,
    employee_update_view,
    get_employees_from_db,
    EmployeeCreateView,
)

urlpatterns = [
    path("get_employees_from_db/", get_employees_from_db, name="get_employees_from_db"),
    path("list/", EmployeeListView.as_view(), name="employees-list"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employees-detail"),
    path("<int:pk>/update/", employee_update_view, name="employee-update"),
    path("create/", EmployeeCreateView.as_view(), name="employee-create"),
]
