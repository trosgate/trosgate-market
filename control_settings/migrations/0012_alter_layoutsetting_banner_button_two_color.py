# Generated by Django 3.2.8 on 2022-10-16 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_settings', '0011_auto_20221015_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layoutsetting',
            name='banner_button_two_color',
            field=models.CharField(blank=True, default='light', help_text="Put your bootstrap color here to decorate Hero Button 2. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes", max_length=100, null=True, verbose_name='Hero Button2 Color'),
        ),
    ]
