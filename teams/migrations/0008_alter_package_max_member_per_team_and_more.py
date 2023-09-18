# Generated by Django 4.1.9 on 2023-09-16 17:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_alter_package_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='max_member_per_team',
            field=models.PositiveIntegerField(default=1, help_text='A freelancer can invite upt this number inclusive', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)], verbose_name='Max Member per Team'),
        ),
        migrations.AlterField(
            model_name='package',
            name='monthly_offer_contracts_per_team',
            field=models.PositiveIntegerField(default=5, help_text="Clients can view team member's profile and send offer Contracts up to 100 monthly", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Monthly Offer Contracts'),
        ),
    ]
