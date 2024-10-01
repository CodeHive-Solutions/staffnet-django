# urls for the employees app.

from django.urls import path
from .views import get_employees_from_db, EmployeeListView, EmployeeDetailView

urlpatterns = [
    path("get_employees_from_db/", get_employees_from_db, name="get_employees_from_db"),
    path("list/", EmployeeListView.as_view(), name="employee_list"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employee_detail"),
]
