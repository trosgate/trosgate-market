# Generated by Django 3.2.8 on 2022-08-09 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0005_alter_contractor_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contractsclient', to='contract.contractor', verbose_name='External Client'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='contractsauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
    ]