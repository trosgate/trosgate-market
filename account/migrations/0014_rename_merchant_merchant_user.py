# Generated by Django 3.2.8 on 2023-03-07 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20230306_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchant',
            old_name='merchant',
            new_name='user',
        ),
    ]
