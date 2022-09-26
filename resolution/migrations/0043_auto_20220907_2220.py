# Generated by Django 3.2.8 on 2022-09-07 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0042_alter_proposalresolution_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractresolution',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type'),
        ),
        migrations.AlterField(
            model_name='projectresolution',
            name='status',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type'),
        ),
    ]