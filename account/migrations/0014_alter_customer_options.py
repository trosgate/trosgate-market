# Generated by Django 3.2.8 on 2022-10-07 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_delete_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ('-date_joined',), 'verbose_name': 'User Manager', 'verbose_name_plural': 'User Manager'},
        ),
    ]