# Generated by Django 3.2.8 on 2022-07-29 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_auto_20220725_0003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentrequest',
            options={'ordering': ['-created_at'], 'verbose_name': 'Payment Request', 'verbose_name_plural': 'Payment Request'},
        ),
    ]
