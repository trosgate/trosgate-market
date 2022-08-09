# Generated by Django 3.2.8 on 2022-08-04 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_alter_paymentrequest_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Requested On'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='payday',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Payment Due'),
        ),
    ]
