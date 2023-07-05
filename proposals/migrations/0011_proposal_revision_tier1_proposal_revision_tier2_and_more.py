# Generated by Django 4.1.9 on 2023-07-04 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0010_proposal_salary_tier1_proposal_salary_tier2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='revision_tier1',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Revision Tier1'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='revision_tier2',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Revision Pricing'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='revision_tier3',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Revision Pricing'),
        ),
    ]
