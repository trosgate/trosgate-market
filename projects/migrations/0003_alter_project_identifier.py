# Generated by Django 3.2.8 on 2023-05-21 21:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='identifier',
            field=models.URLField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Identifier'),
        ),
    ]
