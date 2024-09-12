# Generated by Django 5.1 on 2024-09-12 15:53

import employees.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0021_alter_employee_civil_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=employees.models.UpperEmailField(max_length=254, null=True, unique=True, verbose_name='Correo Electrónico'),
        ),
    ]
