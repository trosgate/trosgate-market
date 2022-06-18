# Generated by Django 3.2.8 on 2022-06-16 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_proposalchat_proposal'),
        ('resolution', '0026_remove_proposalresolution_proposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalresolution',
            name='proposal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resolutionproposal', to='proposals.proposal', verbose_name='Proposal'),
            preserve_default=False,
        ),
    ]
