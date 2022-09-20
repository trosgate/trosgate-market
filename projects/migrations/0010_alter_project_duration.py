# Generated by Django 3.2.8 on 2022-09-19 19:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20220919_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='duration',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now, help_text='deadline for expiration of project', verbose_name='Duration'),
            preserve_default=False,
        ),
    ]
