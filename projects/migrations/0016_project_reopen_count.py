# Generated by Django 3.2.8 on 2022-10-01 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_delete_projectlanguagerequired'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='reopen_count',
            field=models.PositiveSmallIntegerField(choices=[(0, '☆☆☆☆☆'), (1, '★☆☆☆☆'), (2, '★★☆☆☆'), (3, '★★★☆☆'), (4, '★★★★☆'), (5, '★★★★★')], default=0, verbose_name='Reopen Count'),
        ),
    ]
