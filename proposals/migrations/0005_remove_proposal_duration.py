# Generated by Django 3.2.8 on 2022-06-12 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20220611_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='duration',
        ),
    ]