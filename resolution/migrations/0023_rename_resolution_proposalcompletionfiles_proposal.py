# Generated by Django 3.2.8 on 2022-06-16 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0022_alter_proposalreview_resolution'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposalcompletionfiles',
            old_name='resolution',
            new_name='proposal',
        ),
    ]
