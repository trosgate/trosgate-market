# Generated by Django 3.2.8 on 2022-08-07 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20220807_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='CEO/SuperAdmin'),
        ),
    ]
