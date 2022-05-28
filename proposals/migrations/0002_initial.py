# Generated by Django 3.2.8 on 2022-05-24 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='team',
            field=models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.CASCADE, related_name='proposalteam', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='offercontract',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offercontract', to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
        migrations.AddField(
            model_name='offercontract',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offercontract', to='proposals.proposal', verbose_name='Proposal'),
        ),
        migrations.AddField(
            model_name='offercontract',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offercontract', to='teams.team', verbose_name='Team'),
        ),
    ]