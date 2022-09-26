# Generated by Django 3.2.8 on 2022-08-30 12:31

import django.core.validators
from django.db import migrations, models
import proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0008_proposalchat_proposal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='thumbnail',
            field=models.ImageField(help_text="image must be any of these 'JPEG','JPG','PNG','PSD', and dimension 820x312", upload_to=proposals.models.proposal_images_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'JPEG', 'PNG', 'PSD'])], verbose_name='Thumbnail'),
        ),
    ]