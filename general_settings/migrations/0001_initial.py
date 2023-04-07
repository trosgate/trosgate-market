# Generated by Django 3.2.8 on 2023-04-07 18:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields
import general_settings.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutoLogoutSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(blank=True, default='Auto Logout System', max_length=50, verbose_name='Preview')),
                ('warning_time_schedule', models.PositiveIntegerField(blank=True, default='2', help_text='By default the system will attempt to logout user every 2hrs with a prompt. You can change it in hours or days', verbose_name='Warning Time')),
                ('interval', models.CharField(blank=True, default='+2 Hours', help_text='The period of time user can extend to remain logged-in before another warning', max_length=10, verbose_name='Extension Interval')),
            ],
            options={
                'verbose_name': 'Logout Control',
                'verbose_name_plural': 'Logout Control',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Category field is Required', max_length=50, unique=True, verbose_name='Name')),
                ('icon', models.ImageField(default='categories/category.png', upload_to='categories/', verbose_name='Icon')),
                ('preview', models.TextField(blank=True, help_text='Summarized info about your category', max_length=60, null=True, verbose_name='Preview')),
                ('visible', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=False)),
                ('slug', models.SlugField(verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Currency Name')),
                ('code', models.CharField(default='USD', max_length=10, verbose_name='Code')),
                ('symbol', models.CharField(max_length=10, verbose_name='Currency')),
                ('supported', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Supported')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Order Priority')),
                ('default', models.BooleanField(blank=True, choices=[(False, 'No'), (True, 'Yes')], verbose_name='Default')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Department field is Required', max_length=100, unique=True, verbose_name='Department Name')),
            ],
            options={
                'verbose_name': 'Client Department',
                'verbose_name_plural': 'Clients Department',
            },
        ),
        migrations.CreateModel(
            name='DepositControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(default='All about Deposit configuration', max_length=50, verbose_name='Deposit Settings')),
                ('min_balance', models.PositiveIntegerField(default=0, help_text='User with this minimum balance qualifies to make deposit (restricted to base Zero currency point', validators=[django.core.validators.MinValueValidator(0)], verbose_name='Minimum Balance')),
                ('max_balance', models.PositiveIntegerField(default=2000, help_text='User with this Maximum balance has reached the max limit for further deposit(restricted to 50000 currency points)', validators=[django.core.validators.MaxValueValidator(50000)], verbose_name='Maximum Balance')),
                ('min_deposit', models.PositiveIntegerField(default=20, help_text='Minimum mount client can deposit - (restricted to 20 minimum currency points)', validators=[django.core.validators.MinValueValidator(20)], verbose_name='Minimum Deposit Amount')),
                ('max_deposit', models.PositiveIntegerField(default=500, help_text='Maximum amount client can deposit', validators=[django.core.validators.MaxValueValidator(50000)], verbose_name='Maximum Deposit Amount')),
            ],
            options={
                'verbose_name': 'Deposit Settings',
                'verbose_name_plural': 'Deposit Settings',
            },
        ),
        migrations.CreateModel(
            name='DepositGateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='This is the switch for controlling the deposit gateway appearing to customer', help_text='This is the switch to show or hide deposit gateway buttons', max_length=255, verbose_name='Preview')),
                ('paypal', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='PayPal')),
                ('stripe', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Stripe')),
                ('razorpay', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Razorpay')),
                ('flutterwave', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Flutterwave')),
            ],
            options={
                'verbose_name': 'Deposit Gateway',
                'verbose_name_plural': 'Deposit Gateways',
            },
        ),
        migrations.CreateModel(
            name='DiscountSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(default='Level Based Discount System', max_length=50, verbose_name='Preview')),
                ('level_one_name', models.CharField(default='Level One Discount System', max_length=30, unique=True, verbose_name='Level One(L1)')),
                ('level_one_rate', models.PositiveIntegerField(default=0, help_text='Starting Rate for L1 Discount with minimum default of 0 %', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0)], verbose_name='L1 Rate')),
                ('level_one_start_amount', models.PositiveIntegerField(default=10, help_text='Minimum checkout amount with default of zero(0) currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L1 Amount Start')),
                ('level_one_delta_amount', models.PositiveIntegerField(default=199, help_text='checkout amount delta with default of 199 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L1 Amount Delta')),
                ('level_two_name', models.CharField(default='Level Two Discount System', max_length=30, unique=True, verbose_name='Level Two(L2)')),
                ('level_two_rate', models.PositiveIntegerField(default=3, help_text='Second level Rate for L2 Discount with minimum default of 3%', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='L2 Rate')),
                ('level_two_start_amount', models.PositiveIntegerField(default=300, help_text='Minimum checkout amount with default of 300 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L2 Amount Start')),
                ('level_two_delta_amount', models.PositiveIntegerField(default=499, help_text='checkout amount delta with default of 499 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L2 Amount Delta')),
                ('level_three_name', models.CharField(default='Level Three Discount System', max_length=30, unique=True, verbose_name='Level Three(L3)')),
                ('level_three_rate', models.PositiveIntegerField(default=5, help_text='Medium Rate for L3 Discount with minimum default of 5%', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='L3 Rate')),
                ('level_three_start_amount', models.PositiveIntegerField(default=500, help_text='Minimum checkout amount with default of 500 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L3 Amount Start')),
                ('level_three_delta_amount', models.PositiveIntegerField(default=999, help_text='checkout amount delta with default of 999 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L3 Amount Delta')),
                ('level_four_name', models.CharField(default='Level Four Discount System', max_length=30, unique=True, verbose_name='Level Four(L4)')),
                ('level_four_rate', models.PositiveIntegerField(default=7, help_text='Highest Rate for L4 Discount with minimum default of 7%', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='L4 Rate')),
                ('level_four_start_amount', models.PositiveIntegerField(default=1000, help_text='Minimum checkout Amount with default of 1000 currency points', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(50000)], verbose_name='L4 Amount Start')),
            ],
            options={
                'verbose_name': 'Discount Level System',
                'verbose_name_plural': 'Discount Level System',
            },
        ),
        migrations.CreateModel(
            name='ExachangeRateAPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(blank=True, default='Exchange rate API', max_length=100, null=True, verbose_name='Preamble')),
                ('exchange_rates_api_key', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='grab your key from https://exchangerate-api.com/', max_length=255, null=True, verbose_name='API Key'))),
            ],
            options={
                'verbose_name': 'Exchange Rates API',
                'verbose_name_plural': 'Exchange Rates API',
            },
        ),
        migrations.CreateModel(
            name='HiringFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(default='Freelancer fees and charges', max_length=50, verbose_name='Freelancer fees and charges')),
                ('extcontract_fee_percentage', models.PositiveIntegerField(default=20, help_text='This is the first and final percentage fee per external contract', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='External Contract Fee - (%)')),
                ('contract_fee_percentage', models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per contract up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Contract Fee - (%)')),
                ('contract_fee_extra', models.PositiveIntegerField(default=5, help_text='An extra percentage contract fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Contract Extra Fee - (%)')),
                ('contract_delta_amount', models.PositiveIntegerField(default=300, help_text='The break-point for charging extra Contract fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Contract Break-Point (Value)')),
                ('proposal_fee_percentage', models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per proposal up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Proposal Fee - (%)')),
                ('proposal_fee_extra', models.PositiveIntegerField(default=5, help_text='An extra percentage Proposal fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Proposal Extra Fee - (%)')),
                ('proposal_delta_amount', models.PositiveIntegerField(default=300, help_text='The break-point for charging extra Proposal fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Proposal Break-Point (Value)')),
                ('application_fee_percentage', models.PositiveIntegerField(default=20, help_text='This is the first percentage fee per project applied up to Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Job Applicant Fee - (%)')),
                ('application_fee_extra', models.PositiveIntegerField(default=5, help_text='An extra percentage project hiring fee charged beyond Break-Point amount', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(70)], verbose_name='Job Applicant Extra Fee - (%)')),
                ('application_delta_amount', models.PositiveIntegerField(default=300, help_text='The break-point for charging extra project hiring fee on freelancer total earning', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50000)], verbose_name='Job Applicant Break-Point (Value)')),
            ],
            options={
                'verbose_name': 'Hiring Fee System',
                'verbose_name_plural': 'Hiring Fee System',
            },
        ),
        migrations.CreateModel(
            name='Mailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_hosting_server', django_cryptography.fields.encrypt(models.CharField(blank=True, default='smtp.gmail.com', help_text='E.x: smtp.gmail.com', max_length=255, null=True, verbose_name='Email Hosting Server'))),
                ('email_hosting_server_password', django_cryptography.fields.encrypt(models.CharField(blank=True, default='ngnrfcsozfrxbgfx', max_length=255, null=True, verbose_name='Email Server Password'))),
                ('email_hosting_username', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='This is the email hosting username created', max_length=255, null=True, verbose_name='Email Server Username'))),
                ('from_email', django_cryptography.fields.encrypt(models.CharField(blank=True, help_text='This email will be the site-wide support email for all email sending', max_length=255, null=True, verbose_name='Site-Wide Support Email'))),
                ('email_use_tls', django_cryptography.fields.encrypt(models.BooleanField(blank=True, choices=[(False, 'No'), (True, 'Yes')], default=True, help_text='If your hosting support both SSL and TLS, we recommend the use of TLS', null=True, verbose_name='Use TLS'))),
                ('email_use_ssl', django_cryptography.fields.encrypt(models.BooleanField(blank=True, choices=[(False, 'No'), (True, 'Yes')], default=False, help_text='If SSL is set to "Yes", TLS should be "No", and vise-versa', null=True, verbose_name='Use SSL'))),
                ('email_fail_silently', django_cryptography.fields.encrypt(models.BooleanField(blank=True, choices=[(False, 'Show Error'), (True, 'Hide Error')], default=True, help_text='if you want users to see errors with your misconfiguration, set to "Show Error". We recommend that you Hide Error', null=True, verbose_name='Email Fail Silently'))),
                ('email_hosting_server_port', models.PositiveSmallIntegerField(blank=True, default=587, help_text='Usually 587 but confirm from your hosting company', null=True, verbose_name='Email Server Port')),
                ('email_timeout', models.PositiveSmallIntegerField(blank=True, default=60, help_text='the timeout time for email', null=True, verbose_name='Email Timeout')),
            ],
            options={
                'verbose_name': 'Mailer Settings',
                'verbose_name_plural': 'Mailer Settings',
            },
        ),
        migrations.CreateModel(
            name='Payday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(default='Payday Timelines that users should expect money', help_text='"01 Week" means 7 Days, "02 Weeks" means 14 Days, "03 Weeks" means 21 Days, "01 Month" means 28-30 Days', max_length=100, verbose_name='Preview')),
                ('payday_converter', models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month')], default='three_days', max_length=20, verbose_name='Duration')),
            ],
            options={
                'verbose_name': 'Payday Setting',
                'verbose_name_plural': 'Payday Setting',
            },
        ),
        migrations.CreateModel(
            name='PaymentsControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preview', models.CharField(default='All about Transfer and Withdrawal configuration', max_length=50, verbose_name='Payment Settings')),
                ('min_balance', models.PositiveIntegerField(default=0, help_text='After making transfer or withdrawal, User account cannot fall below this limit $(0 - 200)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(200)], verbose_name='Minimum T/W Balance')),
                ('max_receiver_balance', models.PositiveIntegerField(default=2000, help_text='After making transfer, RECEIVER account cannot fall above this limit $(201 - 2000)', validators=[django.core.validators.MinValueValidator(201), django.core.validators.MaxValueValidator(2100)], verbose_name='Maximum Receiver Balance')),
                ('min_transfer', models.PositiveIntegerField(default=20, help_text='Minimum amount Team Owner/Freelancer can transfer per transaction - $(20 - 200)', validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(200)], verbose_name='Minimum Transfer')),
                ('max_transfer', models.PositiveIntegerField(default=500, help_text='Maximum amount Team Owner/Freelancer can transfer per transaction - $(201 - 2000)', validators=[django.core.validators.MinValueValidator(201), django.core.validators.MaxValueValidator(2100)], verbose_name='Maximum Transfer')),
                ('min_withdrawal', models.PositiveIntegerField(default=20, help_text='Minimum Amont freelancer can withdraw per transaction - $(20 - 200)', validators=[django.core.validators.MinValueValidator(20), django.core.validators.MaxValueValidator(200)], verbose_name='Minimum Withdrawal')),
                ('max_withdrawal', models.PositiveIntegerField(default=500, help_text='Maximum Amont freelancer can withdraw per transaction - $(201 - 2000)', validators=[django.core.validators.MinValueValidator(201), django.core.validators.MaxValueValidator(2100)], verbose_name='Maximum Withdrawal')),
            ],
            options={
                'verbose_name': 'Payment Settings',
                'verbose_name_plural': 'Payment Settings',
            },
        ),
        migrations.CreateModel(
            name='ProposalGuides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.CharField(help_text='Instructions you want to show to customers', max_length=100, unique=True, verbose_name='guide')),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Instruction',
                'verbose_name_plural': 'Instructions',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, help_text='Business Size field is Required', max_length=100, unique=True, verbose_name='Business Size')),
            ],
            options={
                'verbose_name': 'Business Size',
                'verbose_name_plural': 'Business Sizes',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Skill field is Required', max_length=100, unique=True, verbose_name='Skill')),
            ],
        ),
        migrations.CreateModel(
            name='StorageBuckets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='Local Storage and Amazon S3 Configuration', max_length=100, verbose_name='Storages')),
                ('bucket_name', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100, null=True, verbose_name='Bucket Name'))),
                ('access_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100, null=True, verbose_name='S3 Access Key'))),
                ('secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=100, null=True, verbose_name='S3 Secret Key'))),
                ('storage_type', models.BooleanField(choices=[(True, 'Local Storage'), (False, 'Amazon S3 Bucket')], default=True, verbose_name='Storage Type')),
            ],
            options={
                'verbose_name': 'File and Image Storage',
                'verbose_name_plural': 'File and Image Storage',
            },
        ),
        migrations.CreateModel(
            name='SubscriptionGateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='This is the switch for controlling the subscriptions appearing to customer', help_text='This is the switch to show or hide subscription gateway buttons', max_length=255, verbose_name='Preview')),
                ('paypal', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='PayPal')),
                ('stripe', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Stripe')),
                ('razorpay', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Razorpay')),
                ('flutterwave', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, verbose_name='Flutterwave')),
            ],
            options={
                'verbose_name': 'Subscription Gateway',
                'verbose_name_plural': 'Subscription Gateways',
            },
        ),
        migrations.CreateModel(
            name='TestEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', django_cryptography.fields.encrypt(models.CharField(blank=True, default='My Test Email', max_length=20, null=True, verbose_name='Testing Email'))),
                ('test_email', django_cryptography.fields.encrypt(models.EmailField(blank=True, help_text='Test the email settings by sending a Test mail', max_length=100, null=True, verbose_name='Receiver Email'))),
            ],
            options={
                'verbose_name': 'Test Email Settings',
                'verbose_name_plural': 'Test Email',
            },
        ),
        migrations.CreateModel(
            name='WebsiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(blank=True, default='Example', max_length=50, null=True, verbose_name='Site Name')),
                ('tagline', models.CharField(blank=True, default='The Marketplace', max_length=150, null=True, verbose_name='Site Tagline')),
                ('site_description', models.TextField(blank=True, default='The Example Marketplace', max_length=300, null=True, verbose_name='Site Decription')),
                ('site_Logo', models.ImageField(blank=True, default='site/logo.png', null=True, upload_to=general_settings.models.site_path, verbose_name='Site Logo')),
                ('protocol', models.CharField(choices=[('https://', 'Secure:> https://'), ('https://www.', 'Secure https://www'), ('http://', 'Insecure:> http://')], default='https://', help_text='Warning! Make sure you have SSL Certificate for your site before switing to Secure options', max_length=20, verbose_name='Protocol Type')),
                ('site_domain', models.CharField(blank=True, default='example.com', help_text='E.x: example.com', max_length=255, null=True, verbose_name='Website Domain')),
                ('button_color', models.CharField(blank=True, default='purple', help_text="Customize colors for signup, login, any other visitor buttons. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes", max_length=100, null=True, verbose_name='Visitor Buttons')),
                ('navbar_color', models.CharField(blank=True, default='purple', help_text="Customize colors for Navbar. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes", max_length=100, null=True, verbose_name='NavBar Color')),
                ('twitter_url', models.URLField(blank=True, help_text='Enter the full secure url path of your Twitter page', max_length=255, null=True, verbose_name='Twitter Page')),
                ('instagram_url', models.URLField(blank=True, help_text='Enter the full secure url path of your Instagram page', max_length=255, null=True, verbose_name='Instagram Page')),
                ('youtube_url', models.URLField(blank=True, help_text='Enter the full secure url path of your Youtube page', max_length=255, null=True, verbose_name='Youtube Page')),
                ('facebook_url', models.URLField(blank=True, help_text='Enter the full secure url path of your Facebook page', max_length=255, null=True, verbose_name='Facebook Page')),
                ('ad_image', models.ImageField(blank=True, help_text="This will appear on 'proposal ad, project ad and all other ad slots'. image must be any of these: 'JPEG','JPG','PNG','PSD'", null=True, upload_to=general_settings.models.site_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Hero Image')),
                ('brand_ambassador_image', models.ImageField(blank=True, help_text="This will appear to logged-in user on 'About Us Page, Freelancer page, project page'. Size should be 255px x 255px. image must be any of these: 'JPEG','JPG','PNG','PSD'", null=True, upload_to=general_settings.models.site_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Brand Ambassador Image')),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='CurrencyConverter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currencyconverter', to='general_settings.currency', verbose_name='Currency Type')),
            ],
            options={
                'verbose_name': 'Currency Converter',
                'verbose_name_plural': 'Currency Converter',
            },
        ),
    ]
