# Generated by Django 3.2.8 on 2022-06-06 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0011_auto_20220605_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectcompletionfiles',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='projectcompletionfiles',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projectcompletionfiles',
            name='team',
        ),
        migrations.AddField(
            model_name='projectresolution',
            name='completed',
            field=models.BooleanField(choices=[(False, 'Ongoing'), (True, 'Completed')], default=True, verbose_name='Completed'),
        ),
    ]