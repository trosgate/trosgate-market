# Generated by Django 3.2.8 on 2022-08-07 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_alter_client_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientaccount',
            name='reference',
        ),
    ]
