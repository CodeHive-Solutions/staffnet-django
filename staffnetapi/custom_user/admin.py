from django.contrib import admin
from .models import CustomUser


# ! Remember implement a attempts max limit for login
# Register your models here.
admin.site.register(CustomUser)