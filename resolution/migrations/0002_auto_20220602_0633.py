# Generated by Django 3.2.8 on 2022-06-02 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20220602_0627'),
        ('resolution', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectresolution',
            name='purchase',
        ),
        migrations.AddField(
            model_name='projectresolution',
            name='application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projectapplicantsaction', to='transactions.applicationsale', verbose_name='Application'),
            preserve_default=False,
        ),
    ]
