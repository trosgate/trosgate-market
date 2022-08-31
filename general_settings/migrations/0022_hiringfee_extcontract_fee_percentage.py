# Generated by Django 3.2.8 on 2022-08-29 21:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0021_alter_payday_payday_converter'),
    ]

    operations = [
        migrations.AddField(
            model_name='hiringfee',
            name='extcontract_fee_percentage',
            field=models.PositiveIntegerField(default=20, help_text='This is the first and final percentage fee per external contract', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='External Contract Fee - (%)'),
        ),
    ]
