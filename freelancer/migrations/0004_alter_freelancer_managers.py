# Generated by Django 3.2.8 on 2023-06-06 18:06

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='freelancer',
            managers=[
                ('active', django.db.models.manager.Manager()),
            ],
        ),
    ]
