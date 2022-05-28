# Generated by Django 3.2.8 on 2022-05-24 22:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Freelancer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, verbose_name='Gender')),
                ('hourly_rate', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(500)], verbose_name='Hourly Rate')),
                ('tagline', models.CharField(blank=True, max_length=100, verbose_name='Tagline')),
                ('description', models.TextField(blank=True, error_messages={'name': {'max_length': 'Ensure a maximum character of 2000 for description field'}}, max_length=2000, verbose_name='Description')),
                ('brand_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Brand Name')),
                ('support', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('profile_photo', models.ImageField(default='freelancer/avatar5.png', upload_to='freelancer/', verbose_name='Profile Photo')),
                ('banner_photo', models.ImageField(default='freelancer/banner.png', upload_to='freelancer/', verbose_name='Banner Photo')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Residence Address')),
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
                ('image_one', models.ImageField(blank=True, default='freelancer/awards/banner.png', null=True, upload_to='freelancer/awards/', verbose_name='Image 1')),
                ('project_title_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Title 2')),
                ('project_url_two', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Project Url 2')),
                ('image_two', models.ImageField(blank=True, default='freelancer/awards/banner.png', null=True, upload_to='freelancer/awards/', verbose_name='Image 2')),
                ('project_title_three', models.CharField(blank=True, max_length=100, null=True, verbose_name='Project Title 3')),
                ('project_url_three', models.URLField(blank=True, max_length=2083, null=True, verbose_name='Project Url 3')),
                ('image_three', models.ImageField(blank=True, default='freelancer/awards/banner.png', null=True, upload_to='freelancer/awards/', verbose_name='Image 3')),
                ('slug', models.SlugField(blank=True, max_length=30, null=True, verbose_name='Slug')),
                ('active_team_id', models.PositiveIntegerField(default=0, verbose_name='Active Team ID')),
            ],
        ),
        migrations.CreateModel(
            name='FreelancerAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Reference Number')),
                ('available_balance', models.PositiveIntegerField(default=0, help_text='Min of $20 and Max of $500 per transaction', verbose_name='Account Balance')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Freelancer Account',
                'verbose_name_plural': 'Freelancer Account',
            },
        ),
        migrations.CreateModel(
            name='FreelancerAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, choices=[('ceo', 'CEO'), ('co_ceo', 'CO-CEO'), ('general_manager', 'General Manager'), ('marketing_manager', 'Marketing Manager'), ('virtual_assistant', 'Virtual Assistant'), ('sales_rep', 'Sales Rep'), ('analyst', 'Analyst'), ('pro', 'PRO')], default='co_ceo', max_length=50, null=True, verbose_name='Worked As')),
                ('action_choice', models.CharField(blank=True, choices=[('none', 'None'), ('transfer', 'Transfer'), ('withdrawal', 'Withdrawal')], default='none', max_length=50, null=True, verbose_name='Worked As')),
                ('transfer_status', models.BooleanField(choices=[(False, 'Failed'), (True, 'Successful')], default=False, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('narration', models.CharField(blank=True, max_length=100, null=True, verbose_name='Withdrawal Narration')),
                ('debit_amount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Transfer Amount')),
                ('withdraw_amount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Withdraw Amount')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundmanageraccount', to='freelancer.freelanceraccount', verbose_name='Account')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundtransferor', to=settings.AUTH_USER_MODEL, verbose_name='Manager')),
            ],
            options={
                'verbose_name': 'Freelancer Action',
                'verbose_name_plural': 'Freelancer Action',
                'ordering': ('-created_at',),
            },
        ),
    ]