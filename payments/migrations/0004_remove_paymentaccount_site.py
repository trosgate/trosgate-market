# Generated by Django 4.1.9 on 2023-08-27 19:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_paymentaccount_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentaccount',
            name='site',
        ),
    ]
