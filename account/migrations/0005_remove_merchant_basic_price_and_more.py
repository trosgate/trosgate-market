# Generated by Django 4.1.9 on 2023-11-16 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_merchant_basic_price_merchant_max_member_per_team_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchant',
            name='basic_price',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='max_member_per_team',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='max_proposals_allowable_per_team',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='monthly_offer_contracts_per_team',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='monthly_projects_applicable_per_team',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='ordering',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='team_plan',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='team_price',
        ),
    ]