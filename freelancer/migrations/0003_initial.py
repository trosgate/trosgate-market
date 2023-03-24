# Generated by Django 3.2.8 on 2023-03-18 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_settings', '0001_initial'),
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freelancer', '0002_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='freelanceraction',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fundtransferteam', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='freelanceraction',
            name='team_staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fundtransferee', to=settings.AUTH_USER_MODEL, verbose_name='Staff'),
        ),
        migrations.AddField(
            model_name='freelanceraccount',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='freelanceaccmerchant', to='account.merchant', verbose_name='Merchant'),
        ),
        migrations.AddField(
            model_name='freelanceraccount',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='fundtransferuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='business_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='freelancers', to='general_settings.size', verbose_name='Business Size'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='general_settings.department', verbose_name='Department'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='freelancemerchant', to='account.merchant', verbose_name='Merchant'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='skill',
            field=models.ManyToManyField(related_name='freelancerskill', to='general_settings.Skill', verbose_name='General skill'),
        ),
        migrations.AddField(
            model_name='freelancer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='freelancer', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
