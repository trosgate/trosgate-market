# Generated by Django 3.2.8 on 2023-04-07 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_duration', models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month'), ('two_month', '02 Months'), ('three_months', '03 Months'), ('four_months', '04 Months'), ('five_months', '05 Months'), ('six_months', '06 Months')], default='three_days', max_length=20, verbose_name='Duration')),
                ('reaction', models.CharField(choices=[('awaiting', 'Awaiting'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='awaiting', max_length=30, verbose_name='State')),
                ('notes', models.TextField(blank=True, max_length=250, null=True)),
                ('reference', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Reference')),
                ('slug', models.SlugField(max_length=150, null=True, verbose_name='Slug')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('line_one', models.CharField(help_text='Enter your main product or service here', max_length=120, verbose_name='Service Description')),
                ('line_one_quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('line_one_unit_price', models.PositiveIntegerField(default=0, verbose_name='Unit Price')),
                ('line_one_total_price', models.PositiveIntegerField(default=0, verbose_name='Total')),
                ('line_two', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras One')),
                ('line_two_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_two_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_two_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_three', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Two')),
                ('line_three_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_three_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_three_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_four', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Three')),
                ('line_four_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_four_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_four_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_five', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Four')),
                ('line_five_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_five_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_five_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('grand_total', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Grand Total')),
            ],
            options={
                'verbose_name': 'External Contract',
                'verbose_name_plural': 'External Contract',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ContractChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Contract Chat',
                'verbose_name_plural': 'Contract Chat',
                'ordering': ['sent_on'],
            },
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter an official name known for the client', max_length=100)),
                ('email', models.CharField(help_text='Enter Valid Email for client to receive mail', max_length=100, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'External Client',
                'verbose_name_plural': 'External Client',
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='InternalContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_duration', models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month'), ('two_month', '02 Months'), ('three_months', '03 Months'), ('four_months', '04 Months'), ('five_months', '05 Months'), ('six_months', '06 Months')], default='one_day', max_length=20, verbose_name='Duration')),
                ('reaction', models.CharField(choices=[('awaiting', 'Awaiting'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='awaiting', max_length=30, verbose_name='State')),
                ('notes', models.TextField(blank=True, max_length=250, null=True)),
                ('reference', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Reference')),
                ('slug', models.SlugField(blank=True, max_length=350, verbose_name='Slug')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('line_one', models.CharField(max_length=120, verbose_name='Service Description')),
                ('line_one_quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('line_one_unit_price', models.PositiveIntegerField(default=0, verbose_name='Unit Price')),
                ('line_one_total_price', models.PositiveIntegerField(default=0, verbose_name='Total')),
                ('line_two', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras One')),
                ('line_two_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_two_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_two_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_three', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Two')),
                ('line_three_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_three_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_three_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_four', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Three')),
                ('line_four_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_four_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_four_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('line_five', models.CharField(blank=True, default=None, max_length=120, null=True, verbose_name='Service Extras Four')),
                ('line_five_quantity', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('line_five_unit_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Unit Price')),
                ('line_five_total_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Total')),
                ('grand_total', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Grand Total')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internalcontractauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Internal Contract',
                'verbose_name_plural': 'Internal Contracts',
                'ordering': ['-date_created'],
            },
        ),
    ]
