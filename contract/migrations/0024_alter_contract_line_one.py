# Generated by Django 3.2.8 on 2022-10-15 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0023_auto_20221015_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='line_one',
            field=models.CharField(help_text='Enter your main product or service her', max_length=120, verbose_name='Service Description'),
        ),
    ]