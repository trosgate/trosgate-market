# Generated by Django 3.2.8 on 2022-08-21 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0007_auto_20220811_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internalcontract',
            name='reaction',
            field=models.CharField(choices=[('awaiting', 'Awaiting'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='awaiting', max_length=30, verbose_name='State'),
        ),
    ]