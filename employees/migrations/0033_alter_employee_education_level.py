# Generated by Django 5.1 on 2024-09-16 20:42

import employees.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0032_alter_employee_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="education_level",
            field=employees.models.UpperCharField(
                choices=[
                    ("PRIMARIA", "Primaria"),
                    ("BACHILLER", "Bachiller"),
                    ("TECNICO", "Técnico"),
                    ("TECNOLOGO", "Tecnologo"),
                    ("AUXILIAR", "Auxiliar"),
                    ("UNIVERSITARIO", "Universitario"),
                    ("PROFESIONAL", "Profesional"),
                    ("ESPECIALIZACION", "Especialización"),
                ],
                max_length=100,
                verbose_name="Nivel de Educación",
            ),
        ),
    ]
