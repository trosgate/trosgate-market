# Generated by Django 3.2.8 on 2022-08-24 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0002_ticket'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='helpdesk',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['created_at']},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='assisted_by',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='query_type_reference',
        ),
        migrations.AddField(
            model_name='ticket',
            name='product_type',
            field=models.CharField(choices=[('Not Applicable', 'Not Applicable'), ('proposal', 'Proposal'), ('project', 'Project'), ('active', 'Contract')], default='Not Applicable', max_length=50, verbose_name='Product Type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='product_type_reference',
            field=models.CharField(blank=True, help_text='Reference for the product type selected', max_length=50, null=True, verbose_name='Product Reference'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='supported_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='adminsupport', to='account.customer', verbose_name='Support Team'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Time Created'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportersupport', to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Time Modified'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='query_type',
            field=models.CharField(choices=[('general_enquiry', 'General Enquiry'), ('signup_challenge', 'Signin/Signup Issues'), ('password_reset', 'Password Reset'), ('team_invite_issue', 'Team Invitation Issues'), ('team_dispute', 'Team Members Dispute'), ('quiz_q_and_a_issue', 'Quiz, Q&A Issues'), ('checkou_issue', 'Checkout Challenge'), ('ACCOUNT_PAYOUT_ISSUE', 'Payout Account Issue'), ('fees_and_charges', 'Fees and Over-Charges'), ('review_approval_issues', 'Order Review/Approval'), ('order_cancellation_issues', 'Order Cancellation'), ('proposal_issue', 'Proposal Issues'), ('project_issue', 'Project Issues'), ('contract_issue', 'Contract Issues'), ('deposit_challenge', 'Deposit Challenge'), ('withdrawal_challenge', 'Withdrawal Challenge'), ('credit_payment_challenge', 'Freelancer Credit'), ('transfer_challenge', 'Transfer Challenge'), ('system_bug', 'Reporting System Bug'), ('other_issues', 'Other Issues')], default='general_enquiry', max_length=50, verbose_name='Query Type'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reference',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='states',
            field=models.CharField(choices=[('ongoing', 'Ongoing'), ('closed', 'Closed'), ('reopen', 'RE-OPEN')], default='ongoing', max_length=20, verbose_name='Status'),
        ),
    ]