# Generated by Django 3.2.8 on 2023-05-19 23:52

import django.contrib.sites.managers
import django.core.validators
from django.db import migrations, models
import general_settings.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20230519_2127'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='merchant',
            managers=[
                ('curr_merchant', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='banner_photo',
        ),
        migrations.RemoveField(
            model_name='merchant',
            name='company_logo',
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_button_one_color',
            field=models.CharField(blank=True, default='green', help_text="Put your bootstrap color here to decorate Hero Button 1. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes", max_length=100, null=True, verbose_name='Hero Button1 Color'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_button_two_color',
            field=models.CharField(blank=True, default='light', help_text="Put your bootstrap color here to decorate Hero Button 2. Example 'primary' or 'secondary' or 'light' or 'success' . Warning!: Exclude quotation marks when you input color attributes", max_length=100, null=True, verbose_name='Hero Button2 Color'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_color',
            field=models.CharField(blank=True, default='purple', help_text="Put your color here to decorate Hero Banner Background and buttons like signup and login. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes", max_length=100, null=True, verbose_name='Hero Background Color'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_image',
            field=models.ImageField(blank=True, help_text="image must be any of these: 'JPEG','JPG','PNG','PSD'", null=True, upload_to=general_settings.models.site_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Hero Image'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='banner_type',
            field=models.BooleanField(choices=[(False, 'Hero Banner'), (True, 'Royal Banner')], default=False, verbose_name='Banner Activator'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='gateway_title',
            field=models.CharField(blank=True, default='Collection and Payout Methods', max_length=100, null=True, verbose_name='Gateway Title'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='project_subtitle',
            field=models.CharField(blank=True, default='Apply and get Hired', max_length=100, null=True, verbose_name='Div Five Project Subitle'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='project_title',
            field=models.CharField(blank=True, default='Published Jobs', max_length=100, null=True, verbose_name='Div Five Project Title'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='proposal_subtitle',
            field=models.CharField(blank=True, default='Verified Proposals', max_length=100, null=True, verbose_name='Div Three Proposal Subitle'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='proposal_title',
            field=models.CharField(blank=True, default='Explore Proposals', max_length=100, null=True, verbose_name='Div Three Proposal Title'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='show_gateways',
            field=models.BooleanField(default=True, verbose_name='Display Gateway'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='subtitle_block',
            field=models.CharField(default='Consectetur adipisicing elit sed dotem eiusmod tempor incuntes ut labore etdolore maigna aliqua enim.', max_length=150, verbose_name='Banner Subtitle'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='title_block',
            field=models.CharField(default='Hire Experts or Team', max_length=100, verbose_name='Banner Title'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='video_description',
            field=models.CharField(blank=True, default='Hire Experts or Team', max_length=100, null=True, verbose_name='Royal Video Description'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='video_title',
            field=models.CharField(blank=True, default='See For Yourself!', max_length=100, null=True, verbose_name='Royal Video Title'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='video_url',
            field=models.URLField(blank=True, help_text='Your can Paste your Youtube or Vimeo video url here to embed. Only secured url allowed', null=True, verbose_name='Royal embed Video'),
        ),
    ]