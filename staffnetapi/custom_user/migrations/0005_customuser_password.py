# Generated by Django 5.1 on 2024-09-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0004_alter_customuser_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='password',
            field=models.CharField(default=1, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
