# Generated by Django 3.2.8 on 2022-10-16 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_auto_20221016_2211'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sponsor',
        ),
        migrations.DeleteModel(
            name='Sponsorship',
        ),
        migrations.RemoveField(
            model_name='investor',
            name='pass_code',
        ),
    ]