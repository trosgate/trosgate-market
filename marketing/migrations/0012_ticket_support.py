# Generated by Django 3.2.8 on 2022-08-25 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketing', '0011_auto_20220825_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='support',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='firstticketsupport', to=settings.AUTH_USER_MODEL, verbose_name='Support'),
        ),
    ]
