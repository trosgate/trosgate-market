# Generated by Django 3.2.8 on 2023-06-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20230606_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='category',
            field=models.CharField(choices=[('proposal', 'Proposal'), ('project', 'Project'), ('contract', 'Contract'), ('excontract', 'Ex-Contract')], default='', max_length=20, verbose_name='Purchase Category'),
        ),
    ]
