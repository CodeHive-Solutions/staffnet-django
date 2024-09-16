# Generated by Django 5.1 on 2024-09-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_delete_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='compensationfund',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='healthprovider',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='management',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='pensionfund',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
