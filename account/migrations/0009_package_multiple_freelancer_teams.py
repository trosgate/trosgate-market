# Generated by Django 3.2.8 on 2023-03-20 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_package_max_users_sitewide'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='multiple_freelancer_teams',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False, help_text='Each freelancer can create multiple teams', verbose_name='Multiple teams per Freelancer'),
        ),
    ]