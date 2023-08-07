# Generated by Django 4.1.9 on 2023-08-04 17:37

import django.core.files.storage
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import resolution.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_alter_merchant_project_type'),
        ('transactions', '0012_alter_applicationsale_status_and_more'),
        ('resolution', '0002_auto_20230606_2146'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text="Supported attachments: 'ZIP', 'RAR','JPEG','JPG','PNG','PSD'", null=True, storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\kateygh\\Desktop\\multitenants\\attachments/'), upload_to=resolution.models.jobs_storage, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ZIP', 'RAR', 'JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('review_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Review Title')),
                ('review_message', models.TextField(blank=True, max_length=650, null=True, verbose_name='Review Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('review_status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], verbose_name='Confirm Work')),
                ('review_date', models.DateTimeField(blank=True, null=True, verbose_name='Reviewed On')),
                ('cancel_type', models.CharField(choices=[('team_exceeded_deadline', 'Team Exceeded Deadline'), ('team_abandoned_work', 'Team Abandoned Work'), ('team_not_responding', 'Team not Responding to Chat'), ('team_is_abusive', 'Team is Abusive'), ('ordered_wrong_product', 'I Ordered Wrong Product'), ('different_product_delivered', 'A different product delivered')], default='team_exceeded_deadline', max_length=100, verbose_name='Issue Type')),
                ('cancel_status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=100, verbose_name='Status')),
                ('cancel_message', models.TextField(max_length=500, verbose_name='Additional Message')),
                ('cancelled_at', models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.merchant', verbose_name='Merchant')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposaljobs', to='transactions.proposalsale', verbose_name='Proposal Sold')),
            ],
            options={
                'verbose_name': 'Proposal File',
                'verbose_name_plural': 'Proposal Files',
                'ordering': ('-created_at',),
            },
        ),
        migrations.RemoveField(
            model_name='applicationreview',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='contractcancellation',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='contractcompletionfiles',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='contractresolution',
            name='contract_sale',
        ),
        migrations.RemoveField(
            model_name='contractresolution',
            name='team',
        ),
        migrations.RemoveField(
            model_name='contractreview',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='extcontractresolution',
            name='contract_sale',
        ),
        migrations.RemoveField(
            model_name='extcontractresolution',
            name='team',
        ),
        migrations.RemoveField(
            model_name='extcontractreview',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='projectcompletionfiles',
            name='application',
        ),
        migrations.RemoveField(
            model_name='projectresolution',
            name='application',
        ),
        migrations.RemoveField(
            model_name='projectresolution',
            name='team',
        ),
        migrations.RemoveField(
            model_name='proposalcancellation',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='proposalcompletionfiles',
            name='proposal',
        ),
        migrations.RemoveField(
            model_name='proposalresolution',
            name='proposal_sale',
        ),
        migrations.RemoveField(
            model_name='proposalresolution',
            name='team',
        ),
        migrations.RemoveField(
            model_name='proposalreview',
            name='resolution',
        ),
        migrations.DeleteModel(
            name='ApplicationCancellation',
        ),
        migrations.DeleteModel(
            name='ApplicationReview',
        ),
        migrations.DeleteModel(
            name='ContractCancellation',
        ),
        migrations.DeleteModel(
            name='ContractCompletionFiles',
        ),
        migrations.DeleteModel(
            name='ContractResolution',
        ),
        migrations.DeleteModel(
            name='ContractReview',
        ),
        migrations.DeleteModel(
            name='ExtContractResolution',
        ),
        migrations.DeleteModel(
            name='ExtContractReview',
        ),
        migrations.DeleteModel(
            name='ProjectCompletionFiles',
        ),
        migrations.DeleteModel(
            name='ProjectResolution',
        ),
        migrations.DeleteModel(
            name='ProposalCancellation',
        ),
        migrations.DeleteModel(
            name='ProposalCompletionFiles',
        ),
        migrations.DeleteModel(
            name='ProposalResolution',
        ),
        migrations.DeleteModel(
            name='ProposalReview',
        ),
    ]
