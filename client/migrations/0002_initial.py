# Generated by Django 4.1.9 on 2023-09-16 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('general_settings', '0001_initial'),
        ('client', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='business_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='general_settings.size', verbose_name='Business Size'),
        ),
        migrations.AddField(
            model_name='client',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general_settings.department', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='client',
            name='employees',
            field=models.ManyToManyField(blank=True, default=None, related_name='employeefreelancer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clientmerchant', to='account.merchant', verbose_name='Merchant'),
        ),
        migrations.AddField(
            model_name='client',
            name='skill',
            field=models.ManyToManyField(related_name='clientskill', to='general_settings.skill', verbose_name='skill'),
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL, verbose_name='Client'),
        ),
    ]
