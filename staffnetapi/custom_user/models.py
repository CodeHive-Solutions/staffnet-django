from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    information = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="user",
        verbose_name="Empleado",
        help_text="Seleccione qué empleado está relacionado con este usuario",
    )
    password = None
    last_login = None
    first_name = None
    last_name = None
    email = None
    date_joined = None

    def is_staff(self):
        return True
