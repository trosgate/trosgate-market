# Generated by Django 4.1.9 on 2023-11-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_subscription_customer_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='reference',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Reference'),
        ),
    ]
