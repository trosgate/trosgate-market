# Generated by Django 3.2.8 on 2022-09-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_auto_20220915_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaction',
            name='reference',
            field=models.CharField(blank=True, help_text='This is a unique number assigned for audit purposes', max_length=15, null=True, verbose_name='Ref Number'),
        ),
    ]