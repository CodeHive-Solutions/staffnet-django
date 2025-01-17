# Generated by Django 5.1 on 2024-09-13 16:41

from django.db import migrations, models

import employees.models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0024_employee_memo_1_employee_memo_2_employee_memo_3"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="contract_type",
            field=employees.models.models.CharField(
                choices=[
                    ("TERMINO INDEFINIDO", "Termino Indefinido"),
                    ("OBRA O LABOR", "Obra o Labor"),
                    ("PRESTACION DE SERVICIOS", "Prestación de Servicios"),
                    ("APRENDIZAJE", "Aprendizaje"),
                ],
                max_length=100,
                verbose_name="Tipo de Contrato",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="stratum",
            field=models.CharField(
                choices=[
                    ("1", "1"),
                    ("2", "2"),
                    ("3", "3"),
                    ("4", "4"),
                    ("5", "5"),
                    ("6", "6"),
                ],
                max_length=1,
                verbose_name="Estrato",
            ),
        ),
    ]
