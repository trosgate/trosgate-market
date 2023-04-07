# Generated by Django 3.2.8 on 2023-04-07 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_settings', '0001_initial'),
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debug_balance', models.PositiveIntegerField(default=0, verbose_name='Pending Balance')),
                ('available_balance', models.PositiveIntegerField(default=0, verbose_name='Account Balance')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clientactmerchant', to='account.merchant', verbose_name='Merchant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='clientfunduser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Client Account',
                'verbose_name_plural': 'Client Account',
                'ordering': ('user__pk',),
            },
        ),
        migrations.CreateModel(
            name='ClientAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('narration', models.CharField(blank=True, max_length=100, null=True, verbose_name='Narration')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='Amount')),
                ('deposit_fee', models.PositiveIntegerField(default=0, verbose_name='Deposit Fee')),
                ('status', models.BooleanField(choices=[(False, 'Failed'), (True, 'Paid')], default=False, verbose_name='Status')),
                ('gateway', models.CharField(max_length=20, verbose_name='Payment Method')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Deposited On')),
                ('reference', models.CharField(blank=True, help_text='This is a unique number assigned for audit purposes', max_length=15, verbose_name='Ref Number')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clientfundaccount', to='client.clientaccount', verbose_name='Account')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='merchantaction', to='account.merchant', verbose_name='Merchant')),
            ],
            options={
                'verbose_name': 'Deposit Ejournal',
                'verbose_name_plural': 'Deposit Ejournal',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, verbose_name='Gender')),
                ('tagline', models.CharField(blank=True, max_length=100, verbose_name='Tagline')),
                ('description', models.TextField(blank=True, error_messages={'name': {'max_length': 'A maximum of 2000 words required'}}, max_length=2000, verbose_name='Description')),
                ('brand_name', models.CharField(blank=True, max_length=60, null=True, verbose_name='Brand Name')),
                ('profile_photo', models.ImageField(default='client/avatar5.png', upload_to='client/', verbose_name='Profile Photo')),
                ('company_logo', models.ImageField(default='client/logo.png', upload_to='client/', verbose_name='Brand Logo')),
                ('banner_photo', models.ImageField(default='client/banner.png', upload_to='client/', verbose_name='Banner Photo')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Residence Address')),
                ('announcement', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Announcement')),
                ('business_size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='general_settings.size', verbose_name='Business Size')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general_settings.department', verbose_name='Department')),
                ('employees', models.ManyToManyField(blank=True, default=None, related_name='employeefreelancer', to=settings.AUTH_USER_MODEL)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clientmerchant', to='account.merchant', verbose_name='Merchant')),
                ('skill', models.ManyToManyField(related_name='clientskill', to='general_settings.Skill', verbose_name='skill')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='Client')),
            ],
            options={
                'verbose_name': 'Client Profile',
                'verbose_name_plural': 'Client Profile',
            },
        ),
    ]
