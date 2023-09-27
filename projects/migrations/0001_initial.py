# Generated by Django 4.1.9 on 2023-09-21 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_settings', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(help_text='title field is Required', max_length=255, unique=True, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('preview', models.CharField(error_messages={'name': {'max_length': 'Preview field is required with maximum of 250 characters'}}, max_length=255, verbose_name='Preview')),
                ('status', models.CharField(choices=[('review', 'Review'), ('active', 'Active'), ('modify', 'Modify'), ('archived', 'Archived')], default='active', max_length=20, verbose_name='Status')),
                ('description', models.TextField(error_messages={'name': {'max_length': 'Description field is required'}}, max_length=3500, verbose_name='Description')),
                ('service_level', models.CharField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], default='basic', error_messages={'name': {'max_length': 'Service Level field is required'}}, max_length=20, verbose_name='Service Level')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('published', models.BooleanField(choices=[(False, 'Unfeature'), (True, 'Feature')], default=False, verbose_name='Featured')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('salary', models.IntegerField(error_messages={'amount': {'max_length': 'Set the salary for this proposal'}}, verbose_name='Price')),
                ('revision', models.PositiveIntegerField(choices=[(1, '1 Time'), (2, '2 Times'), (3, '3 Times'), (4, '4 Times'), (5, '5 Times'), (6, '6 Times'), (7, '7 Times')], default=1, verbose_name='Revision')),
                ('duration', models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], default=3, verbose_name='Duration')),
                ('duration_time', models.DateTimeField(blank=True, help_text='deadline for expiration of project', null=True, verbose_name='Duration Time')),
                ('sample_link', models.URLField(blank=True, help_text='the link must be a verified url', max_length=2083, null=True, verbose_name='Sample Website')),
                ('rating', models.PositiveSmallIntegerField(choices=[(0, '☆☆☆☆☆'), (1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=0, verbose_name='Rating')),
                ('completion_time', models.PositiveIntegerField(choices=[(1, '01 Day'), (2, '02 Days'), (3, '03 Days'), (4, '04 Days'), (5, '05 Days'), (6, '06 Days'), (7, '01 Week'), (14, '02 Weeks'), (21, '03 Weeks'), (30, '01 Month')], default=1, verbose_name='Completion In')),
                ('action', models.BooleanField(default=False, verbose_name='Action')),
                ('reopen_count', models.PositiveSmallIntegerField(default=0, verbose_name='Reopen Count')),
                ('category', models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.RESTRICT, to='general_settings.category', verbose_name='Category')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.merchant', verbose_name='Merchant')),
                ('skill', models.ManyToManyField(error_messages={'name': {'max_length': 'Skill field is required'}}, to='general_settings.skill', verbose_name='Proposal Skills')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ('-created_at',),
                'unique_together': {('slug', 'merchant')},
            },
        ),
    ]
