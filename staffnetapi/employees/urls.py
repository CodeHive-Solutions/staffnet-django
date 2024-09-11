# urls for the employees app.

from django.urls import path
from .views import get_employees_from_db

urlpatterns = [
    path("get_employees_from_db/", get_employees_from_db, name="get_employees_from_db"),
]
