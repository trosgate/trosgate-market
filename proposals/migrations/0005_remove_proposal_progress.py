# Generated by Django 3.2.8 on 2023-03-12 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_proposal_merchant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='progress',
        ),
    ]
