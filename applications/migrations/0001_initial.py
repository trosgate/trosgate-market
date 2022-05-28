# Generated by Django 3.2.8 on 2022-05-24 22:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Message')),
                ('budget', models.IntegerField(default=5, error_messages={'name': {'max_length': 'Set the budget amount (Eg.1000) excluding the currency sign'}}, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(50000)], verbose_name='Budget')),
                ('estimated_duration', models.CharField(choices=[('01 day', '01 Day'), ('02 days', '02 Days'), ('03 days', '03 Days'), ('04 days', '04 Days'), ('05 days', '05 Days'), ('06 days', '06 Days'), ('01 week', '01 Week'), ('02 week', '02 Weeks'), ('03 week', '03 Weeks'), ('01 month', '01 Month'), ('02 month', '02 Months'), ('03 month', '03 Months'), ('04 month', '04 Months'), ('05 month', '05 Months'), ('06 month', '06 Months')], max_length=20, verbose_name='Est. Duration')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20, verbose_name='Status')),
                ('reference', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('applied_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to=settings.AUTH_USER_MODEL, verbose_name='Applicant')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='projects.project', verbose_name='Project')),
            ],
        ),
    ]
