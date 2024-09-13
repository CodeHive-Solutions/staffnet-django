# Generated by Django 5.0.7 on 2024-09-10 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_remove_employee_department_employee_affiliation_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='cell_phone',
            field=models.CharField(default='M', max_length=15, verbose_name='Celular'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='document_type',
            field=models.CharField(choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('TI', 'Tarjeta de Identidad'), ('PP', 'Pasaporte'), ('RC', 'Registro Civil')], default='CC', max_length=2, verbose_name='Tipo de Documento'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1, verbose_name='Género'),
        ),
    ]