# Generated by Django 3.2.8 on 2023-03-20 21:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_package_can_change_domain'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='max_member_per_team',
        ),
        migrations.AddField(
            model_name='package',
            name='can_upsell_teams',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, help_text='Merchant with this package can sell subscription to their freelancers who want to upgrade', verbose_name='Upselling Subscription'),
        ),
        migrations.AddField(
            model_name='package',
            name='max_users_sitewide',
            field=models.PositiveIntegerField(default=1, help_text='Total users including merchant and staffs', validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(1000000)], verbose_name='Max number of users'),
        ),
        migrations.AddField(
            model_name='package',
            name='ssl_activation',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, help_text='Domains on site will be provided with ssl. We recommend actiovation for all domains', verbose_name='SSL Installation'),
        ),
        migrations.AlterField(
            model_name='package',
            name='can_change_domain',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, help_text='Merchant with this package can change domain', verbose_name='Domain Change'),
        ),
    ]
