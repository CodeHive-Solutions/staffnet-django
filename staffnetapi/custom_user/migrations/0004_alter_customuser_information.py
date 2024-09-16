# Generated by Django 5.1 on 2024-09-16 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0003_remove_customuser_date_joined_and_more'),
        ('employees', '0033_alter_employee_education_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='information',
            field=models.ForeignKey(help_text='Seleccione qué empleado está relacionado con este usuario', on_delete=django.db.models.deletion.CASCADE, related_name='user', to='employees.employee', verbose_name='Empleado'),
        ),
    ]
