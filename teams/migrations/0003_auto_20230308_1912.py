# Generated by Django 3.2.8 on 2023-03-08 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_rename_user_merchant_merchant'),
        ('teams', '0002_auto_20230306_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='package',
        ),
        migrations.AddField(
            model_name='team',
            name='merchant',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='teammerchant', to='account.merchant', verbose_name='Merchant'),
            preserve_default=False,
        ),
    ]