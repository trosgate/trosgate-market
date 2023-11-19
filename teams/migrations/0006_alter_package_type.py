# Generated by Django 4.1.9 on 2023-11-19 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_alter_package_verbose_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='type',
            field=models.CharField(choices=[('basic', 'Basic'), ('team', 'Active')], max_length=20, verbose_name='Package Type'),
        ),
    ]