# Generated by Django 3.2.8 on 2023-05-20 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20230520_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='banner_type',
            field=models.CharField(choices=[('slide', 'Carousel Banner'), ('royal', 'Royal Banner'), ('hero', 'Hero Banner')], default='royal', max_length=20, verbose_name='Banner Activator'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='promo_type',
            field=models.CharField(choices=[('zero', 'No Marketing'), ('one', 'Call to Action'), ('two', 'How it Works')], default='two', max_length=10, verbose_name='Marketing Section'),
        ),
    ]