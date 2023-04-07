# Generated by Django 3.2.8 on 2023-04-07 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_initial'),
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freelancer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelanceraction',
            name='gateway',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paymentaccount', to='payments.paymentgateway', verbose_name='Payment Account'),
        ),
        migrations.AddField(
            model_name='freelanceraction',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundtransferor', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='freelanceraction',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='actionmerchant', to='account.merchant', verbose_name='Merchant'),
        ),
    ]
