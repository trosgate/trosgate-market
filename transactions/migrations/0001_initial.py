# Generated by Django 4.1.9 on 2023-09-16 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('contract', '0001_initial'),
        ('proposals', '0001_initial'),
        ('teams', '0001_initial'),
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
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
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
                ('salary_paid', models.PositiveIntegerField(verbose_name='Salary Paid')),
                ('payment_method', models.CharField(blank=True, max_length=200, verbose_name='Payment Method')),
                ('category', models.CharField(choices=[('proposal', 'Proposal'), ('project', 'Project'), ('contract', 'Contract'), ('excontract', 'Ex-Contract')], default='', max_length=20, verbose_name='Purchase Category')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], default='failed', max_length=10, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('client_fee', models.PositiveIntegerField(default=0, verbose_name='Client Fee')),
                ('paypal_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='PayPal Order Key')),
                ('paypal_transaction_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='PayPal Transaction ID')),
                ('reference', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name='Order Key')),
                ('paystack_transaction_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Paystack Transaction ID')),
                ('flutterwave_transaction_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Flutterwave Transaction ID')),
                ('stripe_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='Stripe Order Key')),
                ('razorpay_order_key', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Order Key')),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Payment ID')),
                ('razorpay_signature', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razorpay Signature')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Reference')),
                ('sales_price', models.PositiveIntegerField(default=0, verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(default=0, verbose_name='Applicant Budget')),
                ('disc_sales_price', models.PositiveIntegerField(default=0, verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(default=0, verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(default=0, verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('pending', 'Not Started'), ('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20, verbose_name='Action Type')),
                ('revision', models.PositiveIntegerField(verbose_name='Revision')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration')),
                ('cancel_type', models.CharField(blank=True, choices=[('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type')),
                ('cancel_status', models.CharField(choices=[('not_cancelled', 'Not cancelled'), ('initiated', 'Initiated'), ('approved', 'Approved')], default='not_cancelled', max_length=100, verbose_name='Status')),
                ('cancel_message', models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On')),
                ('package_name', models.CharField(max_length=20, verbose_name='Selected Package')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalhired', to='proposals.proposal', verbose_name='Proposal Hired')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Plan',
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
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'ordering': ('-created_at',),
                'get_latest_by': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ExtContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Reference')),
                ('sales_price', models.PositiveIntegerField(default=0, verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(default=0, verbose_name='Applicant Budget')),
                ('disc_sales_price', models.PositiveIntegerField(default=0, verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(default=0, verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(default=0, verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('pending', 'Not Started'), ('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20, verbose_name='Action Type')),
                ('revision', models.PositiveIntegerField(verbose_name='Revision')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration')),
                ('cancel_type', models.CharField(blank=True, choices=[('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type')),
                ('cancel_status', models.CharField(choices=[('not_cancelled', 'Not cancelled'), ('initiated', 'Initiated'), ('approved', 'Approved')], default='not_cancelled', max_length=100, verbose_name='Status')),
                ('cancel_message', models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontracthired', to='contract.contract', verbose_name='Contract Hired')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ContractSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Reference')),
                ('sales_price', models.PositiveIntegerField(default=0, verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(default=0, verbose_name='Applicant Budget')),
                ('disc_sales_price', models.PositiveIntegerField(default=0, verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(default=0, verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(default=0, verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('pending', 'Not Started'), ('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20, verbose_name='Action Type')),
                ('revision', models.PositiveIntegerField(verbose_name='Revision')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration')),
                ('cancel_type', models.CharField(blank=True, choices=[('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type')),
                ('cancel_status', models.CharField(choices=[('not_cancelled', 'Not cancelled'), ('initiated', 'Initiated'), ('approved', 'Approved')], default='not_cancelled', max_length=100, verbose_name='Status')),
                ('cancel_message', models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracthired', to='contract.contract', verbose_name='Contract Hired')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ApplicationSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(blank=True, max_length=60, null=True, unique=True, verbose_name='Reference')),
                ('sales_price', models.PositiveIntegerField(default=0, verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(default=0, verbose_name='Applicant Budget')),
                ('disc_sales_price', models.PositiveIntegerField(default=0, verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(default=0, verbose_name='Total Earning Fee')),
                ('discount_offered', models.PositiveIntegerField(default=0, verbose_name='Discount Offered')),
                ('total_discount_offered', models.PositiveIntegerField(default=0, verbose_name='Total Discount')),
                ('earning', models.PositiveIntegerField(default=0, verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(default=0, verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('pending', 'Not Started'), ('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20, verbose_name='Action Type')),
                ('revision', models.PositiveIntegerField(verbose_name='Revision')),
                ('duration', models.PositiveIntegerField(verbose_name='Duration')),
                ('cancel_type', models.CharField(blank=True, choices=[('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type')),
                ('cancel_status', models.CharField(choices=[('not_cancelled', 'Not cancelled'), ('initiated', 'Initiated'), ('approved', 'Approved')], default='not_cancelled', max_length=100, verbose_name='Status')),
                ('cancel_message', models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicantprojectapplied', to='projects.project', verbose_name='Project Applied')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
