# Generated by Django 3.2.8 on 2023-03-18 11:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import resolution.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('contract_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractaction', to='transactions.contractsale', verbose_name='Contract Awarded')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvedcontractteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Contract Manager',
                'verbose_name_plural': 'Contract Manager',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ExtContractResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('contract_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontractaction', to='transactions.extcontract', verbose_name='Contract Awarded')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvedextcontractteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Ext-Contract Manager',
                'verbose_name_plural': 'Ext-Contract Manager',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OneClickResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('oneclick_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oneclickaction', to='transactions.oneclickpurchase', verbose_name='One Click Product')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paidoneclickteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'One Click Manager',
                'verbose_name_plural': 'One Click Manager',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('proposal_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalaction', to='transactions.proposalsale', verbose_name='Proposal Sold')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvedproposalteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Proposal Manager',
                'verbose_name_plural': 'Proposal Manager',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(max_length=650, verbose_name='Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], default=True, verbose_name='Confirm Work')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewproposal', to='resolution.proposalresolution', verbose_name='Proposal Review')),
            ],
            options={
                'verbose_name': 'Proposal Review',
                'verbose_name_plural': 'Proposal Review',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalCompletionFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text="image must be any of these 'jpeg','pdf','jpg','png','psd',", null=True, upload_to=resolution.models.proposal_file_directory, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])], verbose_name='Attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicantcompletionfiles', to='resolution.proposalresolution', verbose_name='Proposal File')),
            ],
            options={
                'verbose_name': 'Proposal File',
                'verbose_name_plural': 'Proposal Files',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProposalCancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_type', models.CharField(choices=[('team_exceeded_deadline', 'Team Exceeded Deadline'), ('team_abandoned_work', 'Team Abandoned Work'), ('team_not_responding', 'Team not Responding to Chat'), ('team_is_abusive', 'Team is Abusive'), ('ordered_wrong_product', 'I Ordered Wrong Product'), ('different_product_delivered', 'A different product delivered')], default='team_exceeded_deadline', max_length=100, verbose_name='Issue Type')),
                ('status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=100, verbose_name='Status')),
                ('message', models.TextField(max_length=500, verbose_name='Additional Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cancelproposal', to='resolution.proposalresolution', verbose_name='Proposal')),
            ],
            options={
                'verbose_name': 'Proposal Cancelled',
                'verbose_name_plural': 'Proposal Cancelled',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProjectResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('disputed', 'Disputed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectapplicantsaction', to='transactions.applicationsale', verbose_name='Application Accepted')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvedteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'Application Manager',
                'verbose_name_plural': 'Application Manager',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ProjectCompletionFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text="image must be any of these 'jpeg','pdf','jpg','png','psd',", null=True, upload_to=resolution.models.application_file_directory, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])], verbose_name='Attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicantcompletionfiles', to='resolution.projectresolution', verbose_name='Project File')),
            ],
            options={
                'verbose_name': 'Project File',
                'verbose_name_plural': 'Project Files',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OneClickReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(max_length=650, verbose_name='Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], default=True, verbose_name='Confirm Work')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewoneclick', to='resolution.oneclickresolution', verbose_name='OneClick Review')),
            ],
            options={
                'verbose_name': 'OneClick Review',
                'verbose_name_plural': 'OneClick Review',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OneClickCancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_type', models.CharField(choices=[('team_exceeded_deadline', 'Team Exceeded Deadline'), ('team_abandoned_work', 'Team Abandoned Work'), ('team_not_responding', 'Team not Responding to Chat'), ('team_is_abusive', 'Team is Abusive'), ('ordered_wrong_product', 'I Ordered Wrong Product'), ('different_product_delivered', 'A different product delivered')], default='team_exceeded_deadline', max_length=100, verbose_name='Issue Type')),
                ('status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=100, verbose_name='Status')),
                ('message', models.TextField(max_length=500, verbose_name='Additional Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='canceloneclick', to='resolution.oneclickresolution', verbose_name='Oneclick')),
            ],
            options={
                'verbose_name': 'OneClick Cancelled',
                'verbose_name_plural': 'OneClick Cancelled',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ExtContractReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(max_length=650, verbose_name='Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], default=True, verbose_name='Confirm Work')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewextcontract', to='resolution.extcontractresolution', verbose_name='Contract Review')),
            ],
            options={
                'verbose_name': 'Contract Review',
                'verbose_name_plural': 'Contract Review',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ContractReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(max_length=650, verbose_name='Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], default=True, verbose_name='Confirm Work')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewcontract', to='resolution.contractresolution', verbose_name='Contract Review')),
            ],
            options={
                'verbose_name': 'Contract Review',
                'verbose_name_plural': 'Contract Review',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ContractCompletionFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text="image must be any of these 'jpeg','pdf','jpg','png','psd',", null=True, upload_to=resolution.models.contract_file_directory, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])], verbose_name='Attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractcompletionfiles', to='resolution.contractresolution', verbose_name='Contract File')),
            ],
            options={
                'verbose_name': 'Contract File',
                'verbose_name_plural': 'Contract Files',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ContractCancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_type', models.CharField(choices=[('team_exceeded_deadline', 'Team Exceeded Deadline'), ('team_abandoned_work', 'Team Abandoned Work'), ('team_not_responding', 'Team not Responding to Chat'), ('team_is_abusive', 'Team is Abusive'), ('ordered_wrong_product', 'I Ordered Wrong Product'), ('different_product_delivered', 'A different product delivered')], default='team_exceeded_deadline', max_length=100, verbose_name='Issue Type')),
                ('status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=100, verbose_name='Status')),
                ('message', models.TextField(max_length=500, verbose_name='Additional Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cancelcontract', to='resolution.contractresolution', verbose_name='Contract')),
            ],
            options={
                'verbose_name': 'Contract Cancelled',
                'verbose_name_plural': 'Contract Cancelled',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ApplicationReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('message', models.TextField(max_length=650, verbose_name='Message')),
                ('rating', models.PositiveSmallIntegerField(default=3, verbose_name='Rating')),
                ('status', models.BooleanField(choices=[(False, 'Pending'), (True, 'Completed')], verbose_name='Confirm Work')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewapplication', to='resolution.projectresolution', verbose_name='Applicant Review')),
            ],
            options={
                'verbose_name': 'Application Review',
                'verbose_name_plural': 'Application Review',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ApplicationCancellation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancel_type', models.CharField(choices=[('team_exceeded_deadline', 'Team Exceeded Deadline'), ('team_abandoned_work', 'Team Abandoned Work'), ('team_not_responding', 'Team not Responding to Chat'), ('team_is_abusive', 'Team is Abusive'), ('ordered_wrong_product', 'I Ordered Wrong Product'), ('different_product_delivered', 'A different product delivered')], default='team_exceeded_deadline', max_length=100, verbose_name='Issue Type')),
                ('status', models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='initiated', max_length=100, verbose_name='Status')),
                ('message', models.TextField(max_length=500, verbose_name='Additional Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('resolution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cancelapplication', to='resolution.projectresolution', verbose_name='Application')),
            ],
            options={
                'verbose_name': 'Application Cancelled',
                'verbose_name_plural': 'Application Cancelled',
                'ordering': ('-created_at',),
            },
        ),
    ]
