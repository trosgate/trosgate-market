# Generated by Django 3.2.8 on 2023-04-23 18:41

import ckeditor.fields
import django.contrib.sites.managers
import django.core.validators
from django.db import migrations, models
import django.db.models.manager
import pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('subtitle', models.CharField(blank=True, help_text='subtitle field is optional with length of 200 characters', max_length=200, null=True, verbose_name='Subtitle')),
                ('description', models.TextField(default='This is the description of the about page This is the description of the about page This is the description of the about page This is the description of the about page', help_text='Description max length is 3500', max_length=3500, verbose_name='Description')),
                ('display_stats', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=True, verbose_name='Display Stats')),
                ('banner_type', models.BooleanField(choices=[(True, 'Activate Video'), (False, 'Activate Banner')], default=False, verbose_name='Media Switch')),
                ('ad_image', models.ImageField(blank=True, help_text="image must be any of these: 'JPEG','JPG','PNG','PSD'", null=True, upload_to=pages.models.aboutus_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Ad Image')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('title_block', models.CharField(default='Hire Experts or Team', max_length=100, verbose_name='Banner Title')),
                ('subtitle_block', models.CharField(default='Consectetur adipisicing elit sed dotem eiusmod tempor incuntes ut labore etdolore maigna aliqua enim.', max_length=150, verbose_name='Banner Subtitle')),
                ('banner_color', models.CharField(blank=True, default='purple', help_text="Put your color here to decorate Banner Background and buttons like signup and login. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes", max_length=100, null=True, verbose_name='Banner Background Color')),
                ('banner_button_one_color', models.CharField(blank=True, default='green', help_text="Put your bootstrap color here to decorate Banner Button 1. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes", max_length=100, null=True, verbose_name='Banner Button1 Color')),
                ('banner_button_two_color', models.CharField(blank=True, default='light', help_text="Put your bootstrap color here to decorate Banner Button 2. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes", max_length=100, null=True, verbose_name='Banner Button2 Color')),
                ('banner_image', models.ImageField(blank=True, help_text="image must be any of these: 'JPEG','JPG','PNG','PSD'", null=True, upload_to=pages.models.aboutus_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Hero Image')),
                ('video_url', models.URLField(blank=True, help_text='Enter the full path to your video url on youtube or vimeo etc', max_length=2083, null=True, verbose_name='Embed Video Url')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'About Us Page',
                'verbose_name_plural': 'About Us Page',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Freelancing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('subtitle', models.CharField(blank=True, help_text='subtitle field is optional with length of 200 characters', max_length=200, null=True, verbose_name='Subtitle')),
                ('preview', models.TextField(default=None, help_text='preview max length is 1000', max_length=1000, verbose_name='Preview')),
                ('is_published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=False, verbose_name='Show/Hide')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('thumbnail', models.ImageField(blank=True, default='default-thumbnail.jpg', help_text="image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312", null=True, upload_to='howitworks/thumbnail', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Proposal Thumbnail')),
                ('backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'preview'", max_length=2083, null=True, verbose_name='Back link')),
                ('option_one', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #1')),
                ('option_one_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #1 Description')),
                ('option_two', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #2')),
                ('option_two_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #2 Description')),
                ('option_three', models.CharField(blank=True, max_length=100, null=True, verbose_name='Option #3')),
                ('option_three_description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Option #3 Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'How it Works - Freelancing',
                'verbose_name_plural': 'How it Works - Freelancing',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Hiring',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('subtitle', models.CharField(blank=True, help_text='subtitle field is optional with length of 200 characters', max_length=200, null=True, verbose_name='Subtitle')),
                ('preview', models.TextField(default=None, help_text='preview max length is 1000', max_length=1000, verbose_name='Preview')),
                ('is_published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=False, verbose_name='Show/Hide')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('thumbnail', models.ImageField(blank=True, default='default-thumbnail.jpg', help_text="image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312", null=True, upload_to='howitworks/thumbnail', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Proposal Thumbnail')),
                ('backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'preview'", max_length=1000, null=True, verbose_name='Back link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('ordering', models.PositiveIntegerField(default=0, verbose_name='Order Priority')),
            ],
            options={
                'verbose_name': 'How it Works - Hiring',
                'verbose_name_plural': 'How it Works - Hiring',
                'ordering': ('ordering',),
            },
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salutation', models.CharField(choices=[('mr', 'Mr.'), ('mrs', 'Mrs.'), ('sir', 'Sir'), ('miss', 'Miss'), ('hon', 'Hon'), ('dr', 'Dr.'), ('prof', 'Prof')], default='mr', help_text='How would you like us to address you?', max_length=10, verbose_name='Title')),
                ('verified', models.BooleanField(default=False, verbose_name='Verified')),
                ('myname', models.CharField(max_length=100, verbose_name='Full Name')),
                ('myemail', models.EmailField(max_length=100, verbose_name='Email')),
                ('myconfirm_email', models.EmailField(max_length=100, verbose_name='Confirm Email')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Investors',
                'verbose_name_plural': 'Investors',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='TermsAndConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('quote', models.TextField(blank=True, help_text='This optional text will appear at the top of Description', max_length=350, null=True, verbose_name='Quote')),
                ('description', ckeditor.fields.RichTextField(help_text='Description max length is 3500', max_length=3500, verbose_name='Description')),
                ('is_published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=False, verbose_name='Show/Hide')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Order Priority')),
                ('sites', models.ManyToManyField(to='sites.Site')),
            ],
            options={
                'verbose_name': 'Terms of Service',
                'verbose_name_plural': 'Terms of Service',
                'ordering': ('ordering',),
            },
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('tenants', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
