# Generated by Django 3.2.8 on 2022-10-17 21:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0012_proposalsupport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='progress',
            field=models.PositiveIntegerField(default=0, help_text='Proposal Progress', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(100)], verbose_name='% Progress'),
        ),
    ]
