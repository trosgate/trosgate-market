# Generated by Django 3.2.8 on 2023-05-14 18:08

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title of the blog must be unique - up to max of 255 words', max_length=255, unique=True, verbose_name='Title')),
                ('preview', models.TextField(help_text='Preview of the blog must be unique - up to max of 255 words', max_length=350, verbose_name='Preview')),
                ('backlink', models.URLField(blank=True, help_text="If this notice has detail page to read more, this Optional link will be placed after the last word of 'Preview' to send them there", max_length=2083, null=True, verbose_name='Target Url')),
                ('ordering', models.PositiveIntegerField(default=1, help_text='This determines how each notice will appear to user eg, 1 means topmost position', verbose_name='Ordering')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcement',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='AutoTyPist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Enter up to 30 Characters long', max_length=30, null=True, unique=True, verbose_name='Title')),
                ('is_active', models.BooleanField(choices=[(False, 'Inactive'), (True, 'Active')], default=True, help_text='Make active to show on homepage or Inactive to hide from homepage', verbose_name='Activate')),
                ('ordering', models.PositiveIntegerField(default=1, help_text='This determines how each text will appear to user eg, 1 means first position', verbose_name='Ordering')),
            ],
            options={
                'verbose_name': 'Auto Typist',
                'verbose_name_plural': 'Auto Typist',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title of the blog must be unique', max_length=255, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('introduction', models.TextField(blank=True, help_text='Optional- Must have a maximum of 350 words', max_length=300, null=True, verbose_name='Introduction')),
                ('quote', models.CharField(blank=True, help_text='Optional-Must have a maximum of 200 words', max_length=300, null=True, verbose_name='Special Quote')),
                ('type', models.CharField(choices=[('freelancer', 'Freelancer'), ('client', 'Client')], default=None, max_length=30, verbose_name='Article Type')),
                ('description', ckeditor.fields.RichTextField(error_messages={'name': {'max_length': 'Description field is required'}}, max_length=10000, verbose_name='Details')),
                ('number_of_likes', models.PositiveIntegerField(default=0, verbose_name='Total Likes')),
                ('identifier', models.CharField(blank=True, max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=True, help_text='You can later modify this at your own convenience', verbose_name='Published')),
                ('ordering', models.PositiveIntegerField(default=1, help_text='This determines how each package will appear to user eg, 1 means first position', verbose_name='Ordering')),
                ('thumbnail', models.ImageField(blank=True, default='blog/thumbnail.jpg', help_text="image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312", upload_to='blog', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Blog Thumbnail')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='HelpDesk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('preview', models.TextField(default=None, help_text='preview max length is 1000', max_length=1000, verbose_name='Preview')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('option_one', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #1')),
                ('option_one_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #1 Description')),
                ('option_one_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #1 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #2')),
                ('option_two_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #2 Description')),
                ('option_two_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #2 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_three', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #3')),
                ('option_three_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #3 Description')),
                ('option_three_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #3 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_four', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #4')),
                ('option_four_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #4 Description')),
                ('option_four_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #4 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_five', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #5')),
                ('option_five_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #5 Description')),
                ('option_five_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #5 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_six', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #6')),
                ('option_six_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #6 Description')),
                ('option_six_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #6 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_seven', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #7')),
                ('option_seven_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #7 Description')),
                ('option_seven_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #7 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_eight', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #8')),
                ('option_eight_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #8 Description')),
                ('option_eight_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #8 Description'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_nine', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #9')),
                ('option_nine_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #9 Description')),
                ('option_nine_backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Option #9 Description'", max_length=1500, null=True, verbose_name='Back link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=True, help_text='Only one instance will be shown based on the one that is default', verbose_name='Make Default')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=100, verbose_name='Title')),
                ('slug', models.SlugField(max_length=100, verbose_name='Slug')),
                ('content', models.TextField(max_length=2000, verbose_name='Message')),
                ('reference', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Ticket #')),
                ('states', models.CharField(choices=[('active', 'Active'), ('closed', 'Closed'), ('reopen', 'Reopen')], default='active', max_length=20, verbose_name='Status')),
                ('query_type', models.CharField(choices=[('general_enquiry', '1. General Enquiry'), ('signup_challenge', '2. Signin/Signup Issues'), ('password_reset', '3. Password Reset'), ('team_invite_issue', '4. Team Invitation Issues'), ('team_dispute', '5. Team Members Dispute'), ('quiz_q_and_a_issue', '6. Quiz, Q&A Issues'), ('checkou_issue', '7. Checkout Challenge'), ('Account_payout_issues', '8. Payout Account Issue'), ('fees_and_charges', '9. Fees and Over-Charges'), ('review_approval_issues', '10. Order Review/Approval'), ('order_cancellation_issues', '11. Order Cancellation'), ('credit_payment_challenge', '12. Freelancer Credit'), ('proposal_issue', '13. Proposal Issues'), ('project_issue', '14. Project Issues'), ('contract_issue', '15. Contract Issues'), ('deposit_challenge', '16. Deposit Challenge'), ('withdrawal_challenge', '17. Withdrawal Challenge'), ('transfer_challenge', '18. Transfer Challenge'), ('system_bug', '19. Reporting System Bug'), ('other_issues', '20. Other Issues')], default='general_enquiry', max_length=100, verbose_name='Query Type')),
                ('product_type', models.CharField(choices=[('Not Applicable', 'Not Applicable'), ('proposal', 'Proposal'), ('project', 'Project'), ('active', 'Contract')], default='Not Applicable', max_length=100, verbose_name='Product Type')),
                ('product_type_reference', models.CharField(blank=True, help_text='Reference for the product type selected', max_length=100, null=True, verbose_name='Product Reference')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time Created')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Time Modified')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reportersupport', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('support', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstticketsupport', to=settings.AUTH_USER_MODEL, verbose_name='Current Support')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TicketMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2000, verbose_name='Message')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time Created')),
                ('action', models.BooleanField(choices=[(False, 'Customer Replied'), (True, 'Admin Replied')], default=True, verbose_name='Action')),
                ('link_title_one', models.CharField(blank=True, max_length=100, null=True, verbose_name='Helpful Article Title #1')),
                ('link_title_one_backlink', models.URLField(blank=True, help_text="This Optional link will be placed in the mail to customer'", max_length=2083, null=True, verbose_name='Article Title #1 Backlink')),
                ('link_title_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Helpful Article Title #2')),
                ('link_title_two_backlink', models.URLField(blank=True, help_text="This Optional link will be placed in the mail to customer'", max_length=2083, null=True, verbose_name='Article Title #2 Backlink')),
                ('support', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticketsupport', to=settings.AUTH_USER_MODEL, verbose_name='Support')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickettracker', to='marketing.ticket', verbose_name='Ticket')),
            ],
            options={
                'verbose_name': 'Ticket Reply',
                'verbose_name_plural': 'Ticket Replies',
                'ordering': ['created_at'],
            },
        ),
    ]
