# Generated by Django 5.1.4 on 2025-01-13 17:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0042_alter_contactinformation_cell_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='pant_size',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(6)], verbose_name='Talla de Pantalón'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='responsible_persons',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Personas a Cargo'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='shoe_size',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(20)], verbose_name='Talla de Zapato'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='sons',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)], verbose_name='Número de Hijos'),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='stratum',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)], verbose_name='Estrato'),
        ),
    ]