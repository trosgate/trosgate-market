# Generated by Django 3.2.8 on 2022-09-13 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0002_application_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='application',
            name='slug',
        ),
    ]