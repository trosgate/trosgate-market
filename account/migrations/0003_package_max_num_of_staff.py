# Generated by Django 3.2.8 on 2023-03-18 19:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_merchant_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='max_num_of_staff',
            field=models.PositiveIntegerField(default=1, help_text='Numner of staffs that merchant can invite', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Number of Staff'),
        ),
    ]