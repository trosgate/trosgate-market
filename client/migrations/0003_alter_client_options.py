# Generated by Django 3.2.8 on 2022-07-10 05:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_clientaccount_debug_balance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Client Profile', 'verbose_name_plural': 'Client Profile'},
        ),
    ]
