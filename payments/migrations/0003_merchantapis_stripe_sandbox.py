# Generated by Django 4.1.9 on 2023-07-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantapis',
            name='stripe_sandbox',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=True, verbose_name='Sandbox Mode'),
        ),
    ]
