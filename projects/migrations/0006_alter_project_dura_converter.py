# Generated by Django 3.2.8 on 2022-06-16 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dura_converter',
            field=models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month')], default='01 day', max_length=100, verbose_name='Deadline'),
        ),
    ]