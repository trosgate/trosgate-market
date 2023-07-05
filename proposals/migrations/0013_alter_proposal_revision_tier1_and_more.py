# Generated by Django 4.1.9 on 2023-07-04 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0012_alter_proposal_revision_tier2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='revision_tier1',
            field=models.PositiveIntegerField(choices=[(1, '1 Time'), (2, '2 Times'), (3, '3 Times'), (4, '4 Times'), (5, '5 Times'), (6, '6 Times'), (7, '7 Times')], default=1, verbose_name='Revision Tier1'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='revision_tier2',
            field=models.PositiveIntegerField(choices=[(1, '1 Time'), (2, '2 Times'), (3, '3 Times'), (4, '4 Times'), (5, '5 Times'), (6, '6 Times'), (7, '7 Times')], default=3, verbose_name='Revision Tier2'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='revision_tier3',
            field=models.PositiveIntegerField(choices=[(1, '1 Time'), (2, '2 Times'), (3, '3 Times'), (4, '4 Times'), (5, '5 Times'), (6, '6 Times'), (7, '7 Times')], default=7, verbose_name='Revision Tier3'),
        ),
    ]
