# Generated by Django 3.2.8 on 2023-03-22 19:44

from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_package_multiple_freelancer_teams'),
        ('payments', '0003_merchantapis'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlutterwaveMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flutterwave_public_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='FLUTTERWAVE PUBLISHABLE KEY'))),
                ('flutterwave_secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='FLUTTERWAVE SECRET KEY'))),
                ('flutterwave_subscription_price_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='FLUTTERWAVE SUBSCRIPTION PRICE ID'))),
                ('sandbox', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flutterwavemerchantgw', to='payments.paymentgateway', verbose_name='Merchant')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='flutterwavemerchant', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'Flutterwave Merchant API',
                'verbose_name_plural': 'Flutterwave Merchant API',
            },
        ),
        migrations.CreateModel(
            name='MTNMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mtn_api_user_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='MTN API_USER ID'))),
                ('mtn_api_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='MTN API KEY'))),
                ('mtn_subscription_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='MTN SUBSCRIPTION PRICE ID'))),
                ('mtn_callback_url', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='MTN CALLBACK URL'))),
                ('sandbox', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mtnmerchantgw', to='payments.paymentgateway', verbose_name='Merchant')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='mtnmerchant', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'MTN Merchant API',
                'verbose_name_plural': 'MTN Merchant API',
            },
        ),
        migrations.CreateModel(
            name='PayPalMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_public_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='PAYPAL PUBLISHABLE KEY'))),
                ('paypal_secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='PAYPAL SECRET KEY'))),
                ('paypal_subscription_price_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='PAYPAL SUBSCRIPTION PRICE ID'))),
                ('sandbox', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paypalmerchantgw', to='payments.paymentgateway', verbose_name='Merchant')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='paypalmerchant', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'PayPal Merchant API',
                'verbose_name_plural': 'PayPal Merchant API',
            },
        ),
        migrations.CreateModel(
            name='RazorpayMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_public_key_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='RAZORPAY PUBLISHABLE KEY'))),
                ('razorpay_secret_key_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='RAZORPAY SECRET KEY'))),
                ('razorpay_subscription_price_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='RAZORPAY SUBSCRIPTION PRICE ID'))),
                ('sandbox', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='razorpaymerchantgw', to='payments.paymentgateway', verbose_name='Merchant')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='razorpaymerchant', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'Razorpay Merchant API',
                'verbose_name_plural': 'Razorpay Merchant API',
            },
        ),
        migrations.CreateModel(
            name='StripeMerchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_public_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='STRIPE PUBLISHABLE KEY'))),
                ('stripe_secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='STRIPE SECRET KEY'))),
                ('stripe_webhook_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='STRIPE WEEBHOOK KEY(OPTIONAL)'))),
                ('stripe_subscription_price_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='STRIPE SUBSCRIPTION PRICE ID'))),
                ('sandbox', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode')),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stripemerchantgw', to='payments.paymentgateway', verbose_name='Merchant')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripemerchant', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'Stripe Merchant API',
                'verbose_name_plural': 'Stripe Merchant API',
            },
        ),
        migrations.DeleteModel(
            name='MerchantAPIs',
        ),
    ]