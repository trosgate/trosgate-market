# Generated by Django 3.2.8 on 2022-10-15 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0019_auto_20220908_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='contractor',
            name='phone_Number',
        ),
        migrations.RemoveField(
            model_name='contractor',
            name='postal_code',
        ),
    ]
