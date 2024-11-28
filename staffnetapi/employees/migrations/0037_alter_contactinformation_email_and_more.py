# Generated by Django 5.1.3 on 2024-11-26 13:29

import django.core.validators
import employees.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0036_contactinformation_education_emergencycontact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactinformation',
            name='email',
            field=employees.models.UpperEmailField(db_index=True, max_length=254, null=True, unique=True, verbose_name='Correo Electrónico'),
        ),
        migrations.AlterField(
            model_name='education',
            name='education_level',
            field=employees.models.UpperCharField(choices=[('PRIMARIA', 'Primaria'), ('BACHILLER', 'Bachiller'), ('TÉCNICO', 'Técnico'), ('TECNÓLOGO', 'Tecnólogo'), ('AUXILIAR', 'Auxiliar'), ('UNIVERSITARIO', 'Universitario'), ('PROFESIONAL', 'Profesional'), ('ESPECIALIZACIÓN', 'Especialización')], max_length=100, verbose_name='Nivel de Educación'),
        ),
        migrations.AlterField(
            model_name='employmentdetails',
            name='contract_type',
            field=employees.models.UpperCharField(choices=[('TERMINO INDEFINIDO', 'Termino Indefinido'), ('OBRA O LABOR', 'Obra o Labor'), ('PRESTACIÓN DE SERVICIOS', 'Prestación de Servicios'), ('APRENDIZAJE', 'Aprendizaje')], max_length=100, verbose_name='Tipo de Contrato'),
        ),
        migrations.AlterField(
            model_name='employmentdetails',
            name='salary',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Salario'),
        ),
        migrations.AlterField(
            model_name='employmentdetails',
            name='transportation_allowance',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Auxilio de Transporte'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='identification',
            field=models.PositiveIntegerField(db_index=True, unique=True, validators=[django.core.validators.MinValueValidator(10000)], verbose_name='Identificación'),
        ),
        migrations.AlterField(
            model_name='terminationdetails',
            name='termination_reason',
            field=employees.models.UpperCharField(blank=True, choices=[('BAJA REMUNERACIÓN', 'Baja remuneración'), ('CALAMIDAD FAMILIAR', 'Calamidad familiar'), ('CAMBIO DE ACTIVIDAD', 'Cambio de actividad'), ('CONFLICTOS EN RELACIONES LABORALES', 'Conflictos en relaciones laborales'), ('DESPLAZAMIENTO', 'Desplazamiento'), ('ESTRÉS LABORAL', 'Estrés laboral'), ('FALTA DE HERRAMIENTAS PARA  DESEMPEÑAR LA LABOR', 'Falta de herramientas para  desempeñar la labor'), ('FALTA DE INDUCCIÓN AL INGRESAR', 'Falta de inducción al ingresar'), ('FALTA DE RECONOCIMIENTO', 'Falta de reconocimiento'), ('HORARIO LABORAL', 'Horario laboral'), ('INCOMPATIBILIDAD CON EL JEFE', 'Incompatibilidad con el jefe'), ('MAL AMBIENTE LABORAL', 'Mal ambiente laboral'), ('MOTIVOS DE ESTUDIO', 'Motivos de estudio'), ('MOTIVOS DE SALUD', 'Motivos de salud'), ('MOTIVOS DE VIAJE', 'Motivos de viaje'), ('MOTIVOS PERSONALES', 'Motivos personales'), ('NO HAY OPORTUNIDADES DE CRECIMIENTO LABORAL', 'No hay oportunidades de crecimiento laboral'), ('NO HAY OPORTUNIDADES DE ESTUDIAR', 'No hay oportunidades de estudiar'), ('OTRA OFERTA LABORAL', 'Otra oferta laboral'), ('OTRO', 'Otro'), ('PROBLEMAS PERSONALES', 'Problemas personales'), ('TERMINACIÓN DE CONTRATO APRENDIZAJE', 'Terminación de contrato aprendizaje'), ('TERMINACIÓN DE CONTRATO CON JUSTA CAUSA', 'Terminación de contrato con justa causa'), ('TERMINACIÓN DE CONTRATO POR PERIODO DE PRUEBA', 'Terminación de contrato por periodo de prueba'), ('TERMINACIÓN DE CONTRATO SIN JUSTA CAUSA', 'Terminación de contrato sin justa causa'), ('TERMINACIÓN POR ABANDONO DE PUESTO', 'Terminación por abandono de puesto'), ('TERMINACIÓN POR OBRA O LABOR CONTRATADA ', 'Terminación por obra o labor contratada ')], max_length=100, null=True, verbose_name='Motivo de Terminación'),
        ),
    ]