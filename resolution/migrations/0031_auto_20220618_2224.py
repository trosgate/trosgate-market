# Generated by Django 3.2.8 on 2022-06-18 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0030_auto_20220618_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationreview',
            name='message',
            field=models.TextField(max_length=650, verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='proposalreview',
            name='message',
            field=models.TextField(max_length=650, verbose_name='Message'),
        ),
    ]