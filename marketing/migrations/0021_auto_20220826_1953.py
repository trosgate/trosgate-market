# Generated by Django 3.2.8 on 2022-08-26 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0020_alter_ticket_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='slug',
            field=models.SlugField(default='it-looks-good', max_length=100, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(help_text='title field is Required', max_length=100, verbose_name='Title'),
        ),
    ]
