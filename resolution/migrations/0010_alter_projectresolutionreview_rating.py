# Generated by Django 3.2.8 on 2022-06-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resolution', '0009_auto_20220605_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectresolutionreview',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, "<i class='fa fa-star fill'></i>"), (1, '☆☆☆☆☆'), (2, '★☆☆☆☆'), (3, '★★☆☆☆'), (4, '★★★☆☆'), (5, '★★★★☆'), (6, '★★★★★')], default=3, verbose_name='Rating'),
        ),
    ]
