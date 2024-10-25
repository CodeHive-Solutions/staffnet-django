# Generated by Django 5.1 on 2024-09-18 17:03

import employees.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0034_alter_employee_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="memo_1",
            field=employees.models.UpperCharField(
                blank=True, max_length=300, null=True, verbose_name="Memorando 1"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="memo_2",
            field=employees.models.UpperCharField(
                blank=True, max_length=300, null=True, verbose_name="Memorando 2"
            ),
        ),
        migrations.AlterField(
            model_name="employee",
            name="memo_3",
            field=employees.models.UpperCharField(
                blank=True, max_length=300, null=True, verbose_name="Memorando 3"
            ),
        ),
    ]
