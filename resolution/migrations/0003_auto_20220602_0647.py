# Generated by Django 3.2.8 on 2022-06-02 06:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0002_auto_20220602_0633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectresolution',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='projectresolution',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created On'),
            preserve_default=False,
        ),
    ]
