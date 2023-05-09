# Generated by Django 3.2.8 on 2023-05-02 18:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_package_max_member_per_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='upsell_price',
            field=models.PositiveIntegerField(default=0, help_text='Decide your reasonable price with max limit of 1000', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)], verbose_name='Upsell Price'),
        ),
    ]
