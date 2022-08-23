# Generated by Django 3.2.8 on 2022-08-23 17:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import resolution.models


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0037_contractreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractCompletionFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, help_text="image must be any of these 'jpeg','pdf','jpg','png','psd',", null=True, upload_to=resolution.models.contract_file_directory, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['JPG', 'PDF', 'JPEG', 'PNG', 'PSD'])], verbose_name='Attachment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractcompletionfiles', to='resolution.contractresolution', verbose_name='Contract File')),
            ],
            options={
                'verbose_name': 'Contract File',
                'verbose_name_plural': 'Contract Files',
                'ordering': ('-created_at',),
            },
        ),
    ]
