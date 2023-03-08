# Generated by Django 3.2.8 on 2023-03-06 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_merchant_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='type',
            field=models.PositiveIntegerField(choices=[(1, 'Exempted'), (2, 'Beta'), (3, 'Inactive'), (4, 'Trialing'), (5, 'Active'), (6, 'Past Due'), (7, 'Canceled'), (8, 'Trial Expired')], default=4, verbose_name='Merchant Type'),
        ),
    ]
