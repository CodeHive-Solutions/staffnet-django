# Generated by Django 5.1 on 2024-09-12 15:48

from django.db import migrations

import employees.models


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0020_alter_employee_appointment_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="civil_status",
            field=employees.models.models.CharField(
                choices=[
                    ("SOLTERO(A)", "Soltero(a)"),
                    ("UNION LIBRE", "Unión Libre"),
                    ("CASADO(A)", "Casado(a)"),
                    ("DIVORCIADO(A)", "Divorciado(a)"),
                    ("SEPARADO(A)", "Separado(a)"),
                    ("VIUDO(A)", "Viudo(a)"),
                ],
                max_length=25,
                verbose_name="Estado Civil",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="contract_type",
            field=employees.models.models.CharField(
                choices=[
                    ("TERMINO INDEFINIDO", "Termino Indefinido"),
                    ("TERMINO FIJO", "Termino Fijo"),
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
            name="education_level",
            field=employees.models.models.CharField(
                choices=[
                    ("PRIMARIA", "Primaria"),
                    ("BACHILLER", "Bachiller"),
                    ("TECNICO", "Técnico"),
                    ("TECNOLOGICO", "Tecnológico"),
                    ("AUXILIAR", "Auxiliar"),
                    ("UNIVERSITARIO", "Universitario"),
                    ("PROFESIONAL", "Profesional"),
                    ("ESPECIALIZACION", "Especialización"),
                ],
                max_length=100,
                verbose_name="Nivel de Educación",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="emergency_relationship",
            field=employees.models.models.CharField(
                choices=[
                    ("PADRE", "Padre"),
                    ("MADRE", "Madre"),
                    ("OTRO", "Otro"),
                    ("ABUELO(A)", "Abuelo(a)"),
                    ("AMIGO(A)", "Amigo(a)"),
                    ("HERMANO(A)", "Hermano(a)"),
                    ("ESPOSO(A)", "Esposo(a)"),
                    ("HIJO(A)", "Hijo(a)"),
                    ("TIO(A)", "Tío(a)"),
                    ("PRIMO(A)", "Primo(a)"),
                    ("FAMILIAR", "Familiar"),
                ],
                max_length=100,
                verbose_name="Parentesco Contacto de Emergencia",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="title",
            field=employees.models.models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Título"
            ),
        ),
    ]
