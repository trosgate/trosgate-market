# Generated by Django 3.2.8 on 2022-10-16 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20221016_1551'),
    ]

    operations = [
        # migrations.DeleteModel(
        #     name='Sponsor',
        # ),
        # migrations.DeleteModel(
        #     name='Sponsorship',
        # ),
        migrations.AddField(
            model_name='investor',
            name='status',
            field=models.CharField(choices=[('unverified', 'Unverified'), ('verified', 'Verified')], default='unverified', max_length=10, verbose_name='Title'),
        ),
    ]