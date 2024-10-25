# Generated by Django 5.0.7 on 2024-09-11 19:51

import employees.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "employees",
            "0010_alter_employee_address_alter_employee_business_area_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="corporate_email",
            field=employees.models.UpperEmailField(
                blank=True,
                max_length=254,
                null=True,
                unique=True,
                verbose_name="Correo Electrónico Corporativo",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="email",
            field=employees.models.UpperEmailField(
                max_length=254, unique=True, verbose_name="Correo Electrónico"
            ),
        ),
    ]
