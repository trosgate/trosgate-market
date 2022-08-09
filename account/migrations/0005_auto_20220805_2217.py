# Generated by Django 3.2.8 on 2022-08-05 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20220805_2206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='customer',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='CEO/SuperAdmin Status'),
        ),
    ]
