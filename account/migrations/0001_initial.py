# Generated by Django 3.2.8 on 2022-05-24 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_cryptography.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email Address')),
                ('short_name', models.CharField(max_length=30, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active Status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff Status')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin Status')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('freelancer', 'Freelancer'), ('client', 'Client')], max_length=30, verbose_name='User Type')),
            ],
            options={
                'verbose_name': 'User Manager',
                'verbose_name_plural': 'User Manager',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Country Name')),
                ('country_code', models.CharField(blank=True, max_length=10, verbose_name='Country Code')),
                ('flag', models.ImageField(blank=True, null=True, upload_to='country_flag/', verbose_name='Country Flag')),
                ('ordering', models.PositiveIntegerField(blank=True, null=True, verbose_name='Order Priority')),
                ('supported', models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Supported')),
                ('official_name', models.CharField(blank=True, max_length=100, verbose_name='Official Name')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='TwoFactorAuth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pass_code', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True))),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='twofactorauth', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='State/City')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='states', to='account.country', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
                'ordering': ['country'],
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='countries', to='account.country', verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]