# Generated by Django 5.1 on 2024-09-16 16:39

from django.db import migrations, models

import employees.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "employees",
            "0030_employee_termination_date_employee_termination_type_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="rehire_eligibility",
            field=models.BooleanField(
                default=True, verbose_name="Elegible para Recontratación"
            ),
        ),
        migrations.AddField(
            model_name="employee",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Estado"),
        ),
        migrations.AddField(
            model_name="employee",
            name="termination_reason",
            field=employees.models.models.CharField(
                blank=True,
                choices=[
                    ("BAJA REMUNERACION", "Baja remuneración"),
                    ("CALAMIDAD FAMILIAR", "Calamidad familiar"),
                    ("CAMBIO DE ACTIVIDAD", "Cambio de actividad"),
                    (
                        "CONFLICTOS EN RELACIONES LABORALES",
                        "Conflictos en relaciones laborales",
                    ),
                    ("DESPLAZAMIENTO", "Desplazamiento"),
                    ("ESTRES LABORAL", "Estres laboral"),
                    (
                        "FALTA DE HERRAMIENTAS PARA  DESEMPEÑAR LA LABOR",
                        "Falta de herramientas para  desempeñar la labor",
                    ),
                    (
                        "FALTA DE INDUCCION AL INGRESAR",
                        "Falta de inducción al ingresar",
                    ),
                    ("FALTA DE RECONOCIMIENTO", "Falta de reconocimiento"),
                    ("HORARIO LABORAL", "Horario laboral"),
                    ("INCOMPATIBILIDAD CON EL JEFE", "Incompatibilidad con el jefe"),
                    ("MAL AMBIENTE LABORAL", "Mal ambiente laboral"),
                    ("MOTIVOS DE ESTUDIO", "Motivos de estudio"),
                    ("MOTIVOS DE SALUD", "Motivos de salud"),
                    ("MOTIVOS DE VIAJE", "Motivos de viaje"),
                    ("MOTIVOS PERSONALES", "Motivos personales"),
                    (
                        "NO HAY OPORTUNIDADES DE CRECIMIENTO LABORAL",
                        "No hay oportunidades de crecimiento laboral",
                    ),
                    (
                        "NO HAY OPORTUNIDADES DE ESTUDIAR",
                        "No hay oportunidades de estudiar",
                    ),
                    ("OTRA OFERTA LABORAL", "Otra oferta laboral"),
                    ("OTRO", "Otro"),
                    ("PROBLEMAS PERSONALES", "Problemas personales"),
                    (
                        "TERMINACION DE CONTRATO APRENDIZAJE",
                        "Terminación de contrato aprendizaje",
                    ),
                    (
                        "TERMINACION DE CONTRATO CON JUSTA CAUSA",
                        "Terminación de contrato con justa causa",
                    ),
                    (
                        "TERMINACION DE CONTRATO POR PERIODO DE PRUEBA",
                        "Terminación de contrato por periodo de prueba",
                    ),
                    (
                        "TERMINACION DE CONTRATO SIN JUSTA CAUSA",
                        "Terminación de contrato sin justa causa",
                    ),
                    (
                        "TERMINACION POR ABANDONO DE PUESTO",
                        "Terminación por abandono de puesto",
                    ),
                    (
                        "TERMINACION POR OBRA O LABOR CONTRATADA ",
                        "Terminación por obra o labor contratada ",
                    ),
                ],
                max_length=100,
                null=True,
                verbose_name="Motivo de Terminación",
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="termination_type",
            field=employees.models.models.CharField(
                blank=True,
                choices=[
                    ("VOLUNTARIA", "Voluntaria"),
                    ("INVOLUNTARIA", "Involuntaria"),
                ],
                max_length=100,
                null=True,
                verbose_name="Tipo de Terminación",
            ),
        ),
    ]
