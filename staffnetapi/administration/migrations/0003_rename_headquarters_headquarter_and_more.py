# Generated by Django 4.2.11 on 2024-09-05 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        # ('employees', '0001_initial'),
        ('administration', '0002_alter_campaign_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Headquarters',
            new_name='Headquarter',
        ),
        migrations.RenameModel(
            old_name='SavingFunds',
            new_name='SavingFund',
        ),
    ]
