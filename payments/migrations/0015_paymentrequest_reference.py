# Generated by Django 3.2.8 on 2022-08-04 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_auto_20220804_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='reference',
            field=models.CharField(blank=True, help_text='This is a unique number assigned for audit purposes', max_length=8, verbose_name='Ref Number'),
        ),
    ]