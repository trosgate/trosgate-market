# Generated by Django 3.2.8 on 2022-09-02 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0016_alter_invitation_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='type',
            field=models.CharField(choices=[('founder', 'Founder'), ('internal', 'Internal'), ('external', 'External')], default='founder', max_length=20),
        ),
    ]
