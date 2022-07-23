# Generated by Django 3.2.8 on 2022-07-10 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0004_paymentapis_razorpay_subscription_price_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentapis',
            name='paypal_sandbox',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode'),
        ),
    ]