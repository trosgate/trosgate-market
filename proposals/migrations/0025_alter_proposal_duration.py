# Generated by Django 4.1.9 on 2023-07-15 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0024_alter_proposal_duration_alter_proposal_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='duration',
            field=models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], verbose_name='Duration'),
        ),
    ]
