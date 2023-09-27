# Generated by Django 4.1.9 on 2023-09-21 14:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True, verbose_name='Gender')),
                ('tagline', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tagline')),
                ('description', models.TextField(blank=True, error_messages={'name': {'max_length': 'Ensure a maximum character of 2000 for description field'}}, max_length=2000, verbose_name='Description')),
                ('brand_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Brand Name')),
                ('profile_photo', models.ImageField(default='freelancer/user-login.png', upload_to='freelancer/', verbose_name='Profile Photo')),
                ('banner_photo', models.ImageField(default='freelancer/banner.png', upload_to='freelancer/', verbose_name='Banner Photo')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Residence Address')),
                ('keyskill_one', models.CharField(blank=True, max_length=60, null=True, verbose_name='Key Skill 1')),
                ('key_skill_one_score', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Key Skill 1 Score')),
                ('keyskill_two', models.CharField(blank=True, max_length=60, null=True, verbose_name='Key Skill 2')),
                ('key_skill_two_score', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Key Skill 2 Score')),
                ('keyskill_three', models.CharField(blank=True, max_length=60, null=True, verbose_name='Key Skill 3')),
                ('key_skill_three_score', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Key Skill 3 Score')),
                ('keyskill_four', models.CharField(blank=True, max_length=60, null=True, verbose_name='Key Skill 4')),
                ('key_skill_four_score', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Key Skill 4 Score')),
                ('keyskill_five', models.CharField(blank=True, max_length=60, null=True, verbose_name='Key Skill 5')),
                ('key_skill_five_score', models.PositiveIntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Key Skill 5 Score')),
                ('company_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company Name 1')),
                ('start_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Start Date 1')),
                ('end_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='End Date 1')),
                ('job_position', models.CharField(blank=True, max_length=100, null=True, verbose_name='Job Position 1')),
                ('job_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Job Description 1')),
                ('company_name_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Company Name 2')),
                ('start_date_two', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Start Date 2')),
                ('end_date_two', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='End Date 2')),
                ('job_position_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Job Position 2')),
                ('job_description_two', models.TextField(blank=True, max_length=500, null=True, verbose_name='Job Description 2')),
                ('project_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Title 1')),
                ('project_url', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Project Url 1')),
                ('image_one', models.ImageField(blank=True, null=True, upload_to='freelancer/awards/', verbose_name='Image 1')),
                ('project_title_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Title 2')),
                ('project_url_two', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Project Url 2')),
                ('image_two', models.ImageField(blank=True, null=True, upload_to='freelancer/awards/', verbose_name='Image 2')),
                ('project_title_three', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Title 3')),
                ('project_url_three', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Project Url 3')),
                ('image_three', models.ImageField(blank=True, null=True, upload_to='freelancer/awards/', verbose_name='Image 3')),
                ('slug', models.SlugField(blank=True, max_length=30, null=True, verbose_name='Slug')),
                ('active_team_id', models.PositiveIntegerField(default=0, verbose_name='Active Team ID')),
                ('created', models.BooleanField(default=False, verbose_name='user Created')),
            ],
            options={
                'verbose_name': 'Freelancer Profile',
                'verbose_name_plural': 'Freelancer Profile',
            },
        ),
        migrations.CreateModel(
            name='FreelancerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Reference Number')),
                ('pending_balance', models.PositiveIntegerField(default=0, verbose_name='Pending Balance')),
                ('available_balance', models.PositiveIntegerField(default=0, help_text='Min of $20 and Max of $500 per transaction', verbose_name='Account Balance')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('lock_fund', models.BooleanField(default=False, verbose_name='Lock Fund')),
            ],
            options={
                'verbose_name': 'Freelancer Account',
                'verbose_name_plural': 'Freelancer Account',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='FreelancerAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, choices=[('ceo', 'CEO'), ('co_ceo', 'CO-CEO'), ('general_manager', 'General Manager'), ('marketing_manager', 'Marketing Manager'), ('virtual_assistant', 'Virtual Assistant'), ('sales_rep', 'Sales Rep'), ('analyst', 'Analyst'), ('pro', 'PRO')], default='co_ceo', max_length=50, null=True, verbose_name='Worked As')),
                ('action_choice', models.CharField(blank=True, choices=[('none', 'None'), ('transfer', 'Transfer'), ('withdrawal', 'Withdrawal')], default='none', max_length=50, null=True, verbose_name='Action Type')),
                ('transfer_status', models.BooleanField(choices=[(False, 'Failed'), (True, 'Successful')], default=False, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('narration', models.CharField(blank=True, max_length=100, null=True, verbose_name='Withdrawal Narration')),
                ('debit_amount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Transfer Amount')),
                ('withdraw_amount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Withdraw Amount')),
                ('reference', models.CharField(blank=True, help_text='This is a unique number assigned for audit purposes', max_length=15, verbose_name='Ref Number')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundmanageraccount', to='freelancer.freelanceraccount', verbose_name='Account')),
            ],
            options={
                'verbose_name': 'Freelancer Ejournal',
                'verbose_name_plural': 'Freelancer Ejournal',
                'ordering': ('-id',),
            },
        ),
    ]
