# Generated by Django 3.2.8 on 2023-03-05 22:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('proposals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('todo', 'Todo'), ('completed', 'Completed')], default='todo', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Assign On')),
                ('duty', models.TextField(blank=True, max_length=500, null=True, verbose_name='Job description')),
                ('is_assigned', models.BooleanField(choices=[(False, 'Unassigned'), (True, 'Assigned')], default=False)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignees', to=settings.AUTH_USER_MODEL, verbose_name='Assignee')),
                ('assignor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignors', to=settings.AUTH_USER_MODEL, verbose_name='Assignor')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignproposal', to='proposals.proposal', verbose_name='Proposal')),
            ],
            options={
                'verbose_name': 'Assign Member',
                'verbose_name_plural': 'Assign Member',
                'ordering': ('-modified',),
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(help_text='package type can be eg. BASIC', max_length=50, unique=True, verbose_name='Package Type')),
                ('verbose_type', models.CharField(blank=True, help_text='Customize name for the package. If empty, the default names will be displayed', max_length=50, null=True, unique=True, verbose_name='Branded Name')),
                ('max_member_per_team', models.PositiveIntegerField(default=1, help_text='You can only add up to 4 members for the biggest package', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Max member Per Team')),
                ('monthly_offer_contracts_per_team', models.PositiveIntegerField(default=0, help_text="Clients can view team member's profile and send offer Contracts up to 100 monthly", validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Monthly Offer Contracts')),
                ('max_proposals_allowable_per_team', models.PositiveIntegerField(default=5, help_text='You can add min of 5 and max of 50 Proposals per Team', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(50)], verbose_name='Max Proposals Per Team')),
                ('monthly_projects_applicable_per_team', models.PositiveIntegerField(default=10, help_text='Monthly Jobs Applications with min of 5 and max 50', validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(50)], verbose_name='Monthly Applications Per Team')),
                ('daily_Handshake_mails_to_clients', models.PositiveIntegerField(default=0, help_text='New feature Coming Soon: Here, freelancer team can send followup/ reminder mail per external contract to client. Daily sending will have min of 1 amd max is 3 mails', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)], verbose_name='Daily Contract Mail reminder')),
                ('price', models.PositiveIntegerField(default=0, help_text='Decide your reasonable price with max limit of 1000', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)], verbose_name='Package Price')),
                ('status', models.CharField(choices=[('starter', 'Starter'), ('standard', 'Standard'), ('latest', 'Latest')], default='starter', max_length=20, verbose_name='Package Label')),
                ('is_default', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, help_text="Only 1 package should have a default set to 'Yes'", verbose_name='Make Default')),
                ('ordering', models.PositiveIntegerField(default=1, help_text='This determines how each package will appear to user eg, 1 means first position', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)], verbose_name='Display')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Title')),
                ('notice', models.TextField(max_length=500, verbose_name='Notice')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=20, verbose_name='Team Status')),
                ('package_status', models.CharField(choices=[('default', 'Default'), ('active', 'Active')], default='default', max_length=20, verbose_name='Package Status')),
                ('package_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Package Expiry Date')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('team_balance', models.PositiveIntegerField(default=0, help_text='Team Transaction Balance', verbose_name='Team Balance')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Stripe Customer ID')),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Stripe Subscription ID')),
                ('paypal_customer_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Paypal Customer ID')),
                ('paypal_subscription_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Paypal Subscription ID')),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Razorpay Payment ID')),
                ('razorpay_subscription_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Razorpay Subscription ID')),
                ('razorpay_payment_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Razorpay Short_Link')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teammanager', to=settings.AUTH_USER_MODEL, verbose_name='Team Founder')),
                ('members', models.ManyToManyField(related_name='team_member', to=settings.AUTH_USER_MODEL, verbose_name='Team Members')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='teams.package')),
            ],
        ),
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tasks', models.TextField(blank=True, max_length=200, null=True, verbose_name='Task description')),
                ('is_tracked', models.BooleanField(choices=[(False, 'untracked'), (True, 'Tracked')], default=False)),
                ('minutes', models.PositiveIntegerField(default=0, verbose_name='Time Tracked')),
                ('created_at', models.DateTimeField()),
                ('assigned', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackings', to='teams.assignmember')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackings', to=settings.AUTH_USER_MODEL, verbose_name='Assignee')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackings', to='proposals.proposal', verbose_name='Proposal')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trackings', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TeamChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamsender', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamchats', to='teams.team', verbose_name='Chat Team')),
            ],
            options={
                'ordering': ['sent_on'],
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='Email')),
                ('code', models.CharField(blank=True, max_length=10, verbose_name='Code')),
                ('status', models.CharField(choices=[('invited', 'Invited'), ('accepted', 'Accepted')], default='invited', max_length=20, verbose_name='Status')),
                ('type', models.CharField(choices=[('founder', 'Founder'), ('internal', 'Internal'), ('external', 'External')], default='founder', max_length=20, verbose_name='Invite Type')),
                ('sent_on', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Receiver')),
                ('sender', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='Sender')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='teams.team', verbose_name='Team')),
            ],
        ),
        migrations.AddField(
            model_name='assignmember',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignteam', to='teams.team', verbose_name='Team'),
        ),
    ]
