# Generated by Django 3.2.8 on 2023-03-05 22:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contract', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0001_initial'),
        ('teams', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(blank=True, max_length=200, verbose_name='Payment Method')),
                ('price', models.PositiveIntegerField()),
                ('status', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, verbose_name='Paid')),
                ('customer_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Customer ID')),
                ('subscription_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subscription ID')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='Subscription Start')),
                ('activation_time', models.DateTimeField(blank=True, null=True, verbose_name='Activation Time')),
                ('expired_time', models.DateTimeField(blank=True, null=True, verbose_name='Est. Expiration')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptionteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
                'get_latest_by': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Phone Number')),
                ('country', models.CharField(blank=True, max_length=150, verbose_name='Country')),
                ('salary_paid', models.PositiveIntegerField(verbose_name='Salary Paid')),
                ('client_fee', models.PositiveIntegerField(verbose_name='Client Fee')),
                ('payment_method', models.CharField(blank=True, max_length=200, verbose_name='Payment Method')),
                ('category', models.CharField(choices=[('proposal', 'Proposal'), ('project', 'Project'), ('contract', 'Contract'), ('excontract', 'Ex-Contract')], default='', max_length=20, verbose_name='Purchase Category')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], default='failed', max_length=10, verbose_name='Status')),
                ('unique_reference', models.CharField(blank=True, max_length=100, verbose_name='Unique Reference')),
                ('paypal_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='PayPal Order Key')),
                ('flutterwave_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='Flutterwave Order Key')),
                ('stripe_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='Stripe Order Key')),
                ('razorpay_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Order Key')),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Payment ID')),
                ('razorpay_signature', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Signature')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderclient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.PositiveIntegerField(verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(verbose_name='Total Salary')),
                ('disc_sales_price', models.PositiveIntegerField(verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalhired', to='proposals.proposal', verbose_name='Proposal Hired')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalsales', to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiredproposalteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OneClickPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_paid', models.PositiveIntegerField(verbose_name='Salary Paid')),
                ('total_earning', models.PositiveIntegerField(verbose_name='Total Earning')),
                ('earning_fee', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('payment_method', models.CharField(blank=True, max_length=200, verbose_name='Payment Method')),
                ('category', models.CharField(choices=[('proposal', 'Proposal'), ('contract', 'Contract'), ('externalcontract', 'External Contract')], default='', max_length=20, verbose_name='Purchase Category')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], default='failed', max_length=10, verbose_name='Status')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, verbose_name='Reference')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oneclickclient', to=settings.AUTH_USER_MODEL)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='intoneclickcontract', to='contract.internalcontract', verbose_name='Int Contract')),
                ('extcontract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extoneclickcontract', to='contract.contract', verbose_name='Ext Contract')),
                ('proposal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='oneclickproposal', to='proposals.proposal', verbose_name='Proposal')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oneclickteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'One Click Purchase',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ExtContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.PositiveIntegerField(verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(verbose_name='Contract Total')),
                ('disc_sales_price', models.PositiveIntegerField(verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(verbose_name='Total Earning Fee')),
                ('earning', models.PositiveIntegerField(verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontracthired', to='contract.contract', verbose_name='Contract Hired')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontractsales', to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiredextcontractteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ContractSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.PositiveIntegerField(verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(verbose_name='Contract Total')),
                ('disc_sales_price', models.PositiveIntegerField(verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracthired', to='contract.internalcontract', verbose_name='Contract Hired')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractsales', to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiredcontractteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ApplicationSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.PositiveIntegerField(verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(verbose_name='Applicant Budget')),
                ('disc_sales_price', models.PositiveIntegerField(verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(verbose_name='Earning')),
                ('total_earnings', models.PositiveIntegerField(verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicantprojectapplied', to='projects.project', verbose_name='Project Applied')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicantionsales', to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiredapplicantteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
