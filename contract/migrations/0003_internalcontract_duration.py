# Generated by Django 3.2.8 on 2022-05-24 23:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalcontract',
            name='duration',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='deadline for contract', verbose_name='Completion In'),
            preserve_default=False,
        ),
    ]