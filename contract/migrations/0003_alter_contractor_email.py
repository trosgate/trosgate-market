# Generated by Django 4.1.9 on 2023-09-21 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='email',
            field=models.EmailField(help_text='Enter Valid Email for client to receive mail', max_length=100, unique=True),
        ),
    ]
