# Generated by Django 4.1.9 on 2023-06-29 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_proposal_digital_proposal_salary_tier1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='pricing_tier',
            field=models.CharField(choices=[('salary_tier1', 'Basic'), ('salary_tier2', 'Standard'), ('salary_tier3', 'Premium')], default='salary_tier1', max_length=30, verbose_name='Pricing Tier'),
        ),
    ]
