# Generated by Django 3.2.8 on 2022-08-28 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0008_alter_internalcontract_reaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalcontract',
            name='contract_duration',
            field=models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month'), ('two_month', '02 Months'), ('three_months', '03 Months'), ('four_months', '04 Months'), ('five_months', '05 Months'), ('six_months', '06 Months')], default='one_day', max_length=20, verbose_name='Duration'),
        ),
    ]
