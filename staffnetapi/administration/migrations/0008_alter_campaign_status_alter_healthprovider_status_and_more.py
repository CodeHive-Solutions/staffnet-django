# Generated by Django 5.1 on 2024-09-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_remove_compensationfund_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='healthprovider',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='jobtitle',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='management',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Estado'),
        ),
    ]
