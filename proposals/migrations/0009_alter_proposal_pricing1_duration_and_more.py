# Generated by Django 4.1.9 on 2023-07-04 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_proposal_pricing_proposal_pricing1_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='pricing1_duration',
            field=models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], default=3, verbose_name='Duration Tier1'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='pricing2_duration',
            field=models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], default=5, verbose_name='Duration Tier2'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='pricing3_duration',
            field=models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], default=7, verbose_name='Duration Tier3'),
        ),
    ]