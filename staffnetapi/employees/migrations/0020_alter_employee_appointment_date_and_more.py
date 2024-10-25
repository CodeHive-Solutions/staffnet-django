# Generated by Django 5.1 on 2024-09-12 15:44

import django.core.validators
import employees.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0019_alter_employee_remote_work_application_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="appointment_date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Fecha de Nombramiento"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="identification",
            field=models.PositiveIntegerField(
                unique=True,
                validators=[django.core.validators.MinValueValidator(10000)],
                verbose_name="Identificación",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="last_name",
            field=employees.models.UpperCharField(
                blank=True, max_length=100, null=True, verbose_name="Apellidos"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="pant_size",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Talla de Pantalón",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="shirt_size",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Talla de Camisa",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="shoe_size",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(20),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Talla de Zapato",
            ),
        ),
    ]
