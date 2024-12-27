# urls for the employees app.

from django.urls import path
from .views import (  # UpdateEmployeeView,; get_employees_from_db,
    CreateEmployeeView,
    EmployeeDetailView,
    EmployeeListView,
    get_employees_from_db,
)

# create_employee,

urlpatterns = [
    path("get_employees_from_db/", get_employees_from_db, name="get_employees_from_db"),
    path("list/", EmployeeListView.as_view(), name="employees-list"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employees-detail"),
    path("create/", CreateEmployeeView.as_view(), name="employee-create"),
    # path("<int:pk>/update/", UpdateEmployeeView.as_view(), name="employee-update"),
]
