# Generated by Django 3.2.8 on 2022-06-02 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20220530_2142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='applicationsale',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='contractsale',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='proposalsale',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='salesreporting',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='subscriptionitem',
            options={'ordering': ('-created_at',)},
        ),
    ]