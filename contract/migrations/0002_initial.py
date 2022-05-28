# Generated by Django 3.2.8 on 2022-05-24 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proposals', '0001_initial'),
        ('contract', '0001_initial'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internalcontract',
            name='proposal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internalcontractproposal', to='proposals.proposal', verbose_name='Proposal'),
        ),
        migrations.AddField(
            model_name='internalcontract',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internalcontractteam', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contractors', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='contractor',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractors', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='contractchat',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractclientchat', to='contract.internalcontract', verbose_name='External Client'),
        ),
        migrations.AddField(
            model_name='contractchat',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contractchatsender', to=settings.AUTH_USER_MODEL, verbose_name='Sender'),
        ),
        migrations.AddField(
            model_name='contractchat',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contractteamchat', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contractsclient', to='contract.contractor', verbose_name='External Client'),
        ),
        migrations.AddField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='contractsauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='contract',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractsteam', to='teams.team', verbose_name='Team'),
        ),
        migrations.CreateModel(
            name='InternalContractChat',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('contract.internalcontract',),
        ),
    ]