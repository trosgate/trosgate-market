# Generated by Django 3.2.8 on 2022-10-15 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contract', '0020_auto_20221015_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractors', to=settings.AUTH_USER_MODEL, verbose_name='Invitee'),
        ),
    ]
