# Generated by Django 3.2.8 on 2022-09-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0030_auto_20220916_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptiongateway',
            name='name',
            field=models.CharField(default='This is the switch for controlling the subscriptions appearing to customer', help_text='This is the switch for controlling the subscriptions appearing to customer', max_length=255, unique=True, verbose_name='Preview'),
            preserve_default=False,
        ),
    ]