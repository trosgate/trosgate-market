# Generated by Django 3.2.8 on 2022-08-29 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0009_alter_internalcontract_contract_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='urlcode',
        ),
        migrations.RemoveField(
            model_name='internalcontract',
            name='urlcode',
        ),
    ]
