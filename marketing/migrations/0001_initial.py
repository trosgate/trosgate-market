# Generated by Django 3.2.8 on 2022-05-24 22:47

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(help_text='title of the blog must be unique', max_length=255, unique=True, verbose_name='Content')),
                ('backlink', models.URLField(blank=True, help_text="This Optional link will be placed after the last word of 'Content'", max_length=2083, null=True, verbose_name='Target Url')),
                ('default', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=False, verbose_name='Default')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcement',
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
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='title of the blog must be unique', max_length=255, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('type', models.CharField(choices=[('freelancer', 'Freelancer'), ('client', 'Client')], default=None, max_length=30, verbose_name='Article Type')),
                ('description', ckeditor.fields.RichTextField(error_messages={'name': {'max_length': 'Description field is required'}}, max_length=20000, verbose_name='Description')),
                ('number_of_likes', models.PositiveIntegerField(default=0, verbose_name='Total Likes')),
                ('identifier', models.CharField(blank=True, max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('published', models.BooleanField(choices=[(False, 'Private'), (True, 'Public')], default=True, help_text='You can later modify this at your own convenience', verbose_name='Published')),
                ('ordering', models.PositiveIntegerField(default=1, help_text='This determines how each package will appear to user eg, 1 means first position', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)], verbose_name='Ordering')),
                ('thumbnail', models.ImageField(blank=True, default='blog/thumbnail.jpg', help_text="image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312", upload_to='blog', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Blog Thumbnail')),
                ('category', models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.RESTRICT, related_name='blogcategory', to='general_settings.category', verbose_name='Category')),
                ('created_by', models.ForeignKey(help_text='This blog will be removed if author is deleted', on_delete=django.db.models.deletion.CASCADE, related_name='blogauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('likes', models.ManyToManyField(related_name='bloglikes', to=settings.AUTH_USER_MODEL, verbose_name='Likes')),
                ('tags', models.ManyToManyField(related_name='blogtags', to='general_settings.Skill', verbose_name='Blog Tags')),
            ],
            options={
                'ordering': ['ordering'],
            },
        ),
    ]
