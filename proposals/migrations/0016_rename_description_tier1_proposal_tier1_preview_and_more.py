# Generated by Django 4.1.9 on 2023-07-12 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0015_alter_proposal_salary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='description_tier1',
            new_name='tier1_preview',
        ),
        migrations.RenameField(
            model_name='proposal',
            old_name='description_tier2',
            new_name='tier2_preview',
        ),
        migrations.RenameField(
            model_name='proposal',
            old_name='description_tier3',
            new_name='tier3_preview',
        ),
    ]