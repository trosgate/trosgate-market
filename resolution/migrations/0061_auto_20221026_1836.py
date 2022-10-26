# Generated by Django 3.2.8 on 2022-10-26 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0060_alter_extcontractresolution_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contractresolution',
            options={'ordering': ('-created_at',), 'verbose_name': 'Contract Manager', 'verbose_name_plural': 'Contract Manager'},
        ),
        migrations.AlterModelOptions(
            name='extcontractresolution',
            options={'ordering': ('-created_at',), 'verbose_name': 'Ext-Contract Manager', 'verbose_name_plural': 'Ext-Contract Manager'},
        ),
        migrations.AlterModelOptions(
            name='oneclickresolution',
            options={'ordering': ('-created_at',), 'verbose_name': 'One Click Manager', 'verbose_name_plural': 'One Click Manager'},
        ),
        migrations.AlterModelOptions(
            name='projectresolution',
            options={'ordering': ('-created_at',), 'verbose_name': 'Application Manager', 'verbose_name_plural': 'Application Manager'},
        ),
        migrations.AlterModelOptions(
            name='proposalresolution',
            options={'ordering': ('-created_at',), 'verbose_name': 'Proposal Manager', 'verbose_name_plural': 'Proposal Manager'},
        ),
    ]
