# Generated by Django 3.2.8 on 2022-08-21 12:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0016_auto_20220730_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiringfee',
            name='application_delta_amount',
            field=models.PositiveIntegerField(default=300, help_text='The break-point for charging extra job hiring fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Job Applicant Break-Point (Value)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='application_fee_extra',
            field=models.PositiveIntegerField(default=5, help_text='An extra percentage job hiring fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Job Applicant Extra Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='application_fee_percentage',
            field=models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per Proposal up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Job Applicant Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='contract_delta_amount',
            field=models.PositiveIntegerField(default=300, help_text='The break-point for charging extra Contract fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Contract Break-Point (Value)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='contract_fee_extra',
            field=models.PositiveIntegerField(default=5, help_text='An extra percentage contract fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Contract Extra Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='contract_fee_percentage',
            field=models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per contract up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Contract Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='proposal_delta_amount',
            field=models.PositiveIntegerField(default=300, help_text='The break-point for charging extra Proposal fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Proposal Break-Point (Value)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='proposal_fee_extra',
            field=models.PositiveIntegerField(default=5, help_text='An extra percentage Proposal fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Proposal Extra Fee - (%)'),
        ),
        migrations.AlterField(
            model_name='hiringfee',
            name='proposal_fee_percentage',
            field=models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per proposal up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Proposal Fee - (%)'),
        ),
    ]