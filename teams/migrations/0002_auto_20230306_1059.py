# Generated by Django 3.2.8 on 2023-03-06 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20230306_1059'),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='account.package'),
        ),
        migrations.DeleteModel(
            name='Package',
        ),
    ]