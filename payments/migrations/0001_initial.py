# Generated by Django 3.2.8 on 2022-11-04 18:28

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Amount')),
                ('comment', models.TextField(max_length=200, verbose_name='Credit Comment')),
                ('reference', models.CharField(blank=True, help_text='STAN means System Audit Trail Number', max_length=200, verbose_name='STAN')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Started On')),
                ('status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=20, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Credit Memo',
                'verbose_name_plural': 'Credit Memos',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_account', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Account Number', max_length=100, null=True, verbose_name='Bearer Account/Email'))),
                ('paypal_bearer', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer names', max_length=100, null=True, verbose_name='Bearer names'))),
                ('paypal_country', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer account country. E.g Singapore', max_length=100, null=True, verbose_name='Bearer Country Name'))),
                ('stripe_country', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer account country. E.g Canada', max_length=100, null=True, verbose_name='Bearer Country Name'))),
                ('stripe_bank', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Bank Name - Account Specific', max_length=100, null=True, verbose_name='Bearer Bank Name'))),
                ('stripe_account', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Account Number', max_length=100, null=True, verbose_name='Account Number'))),
                ('stripe_routing', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Routing Number - Country/Bank Specific', max_length=100, null=True, verbose_name='Routing Number'))),
                ('stripe_swift_iban', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Swift code/Iban- Country/Bank Specific', max_length=100, null=True, verbose_name='Swift/Iban code'))),
                ('stripe_bearer', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer names', max_length=150, null=True, verbose_name='Bearer Names'))),
                ('stripe_extra_info', django_cryptography.fields.encrypt(models.TextField(blank=True, help_text='Additional information to be included', max_length=100, null=True, verbose_name='Extra Credentials'))),
                ('flutterwave_type', django_cryptography.fields.encrypt(models.CharField(choices=[('mobilemoney', 'Mobile Money'), ('bank', 'Bank Account')], default='mobilemoney', max_length=20, verbose_name='Flutterwave Account Type'))),
                ('flutterwave_bank', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Bank name - Account Type Specific', max_length=150, null=True, verbose_name='Bearer Bank Names'))),
                ('flutterwave_bearer', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Account names', max_length=150, null=True, verbose_name='Bearer Names'))),
                ('flutterwave_country', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer account country. E.g Nigeria', max_length=100, null=True, verbose_name='Bearer Country Name'))),
                ('flutterwave_account', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Account Number', max_length=100, null=True, verbose_name='Flutterwave Account Number'))),
                ('flutterwave_swift_iban', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Swift code/Iban- Country Specific', max_length=100, null=True, verbose_name='Swift/Iban'))),
                ('flutterwave_extra_info', django_cryptography.fields.encrypt(models.TextField(blank=True, help_text='Additional information to be included', max_length=100, null=True, verbose_name='Extra Credentials'))),
                ('razorpay_bearer', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer Account names', max_length=150, null=True, verbose_name='Razorpay Bearer Names'))),
                ('razorpay_upi', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer UPI ID to receive payment', max_length=100, null=True, verbose_name='Razorpay UPI ID'))),
                ('razorpay_country', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='Bearer account country. E.g India', max_length=100, null=True, verbose_name='Bearer Country Name'))),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Started On')),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Payment Account',
                'verbose_name_plural': 'Payment Account',
            },
        ),
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Amount')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Paid')], default=False, verbose_name='Action Type')),
                ('gateway', models.CharField(max_length=50, verbose_name='Payment Account')),
                ('message', models.TextField(blank=True, max_length=500, null=True, verbose_name='Payment Error Message')),
                ('payday', models.DateTimeField(blank=True, null=True, verbose_name='Payment Due')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Requested On')),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(blank=True, help_text='This is a unique number assigned for audit purposes', max_length=15, verbose_name='Ref Number')),
            ],
            options={
                'verbose_name': 'Payment Request',
                'verbose_name_plural': 'Payment Request',
                'ordering': ['-created_at'],
            },
        ),
    ]
