# Generated by Django 3.2.8 on 2022-09-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0022_auto_20220924_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractsale',
            name='disc_sales_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Discounted Salary'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contractsale',
            name='total_discount_offered',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Discount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contractsale',
            name='total_earning',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Earning'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contractsale',
            name='total_earning_fee_charged',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Earning Fee'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contractsale',
            name='total_sales_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Contract Total'),
            preserve_default=False,
        ),
    ]