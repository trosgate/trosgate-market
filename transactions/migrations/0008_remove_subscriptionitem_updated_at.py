# Generated by Django 3.2.8 on 2022-06-23 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20220623_0112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriptionitem',
            name='updated_at',
        ),
    ]