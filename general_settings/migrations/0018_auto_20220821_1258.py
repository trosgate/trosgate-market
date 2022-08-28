# Generated by Django 3.2.8 on 2022-08-21 12:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0017_auto_20220821_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiringfee',
            name='application_delta_amount',
            field=models.PositiveIntegerField(default=300, help_text='The break-point for charging extra project hiring fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Job Applicant Break-Point (Value)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='application_fee_extra',
            field=models.PositiveIntegerField(default=5, help_text='An extra percentage project hiring fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Job Applicant Extra Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='application_fee_percentage',
            field=models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per project applied up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Job Applicant Fee - (%)'),
        ),
    ]