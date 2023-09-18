# Generated by Django 4.1.9 on 2023-09-16 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_merchant_packages'),
        ('contract', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.merchant', verbose_name='Merchant'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.merchant', verbose_name='Merchant'),
        ),
    ]
