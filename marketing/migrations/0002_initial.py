# Generated by Django 4.1.9 on 2023-08-25 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('general_settings', '0001_initial'),
        ('marketing', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='team',
            field=models.ForeignKey(blank=True, help_text='Only Applicable to Freelancer Queries', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporterteam', to='teams.team', verbose_name='Team'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.RESTRICT, related_name='blogcategory', to='general_settings.category', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='created_by',
            field=models.ForeignKey(help_text='This blog will be removed if author is deleted', on_delete=django.db.models.deletion.CASCADE, related_name='blogauthor', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(related_name='bloglikes', to=settings.AUTH_USER_MODEL, verbose_name='Likes'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(related_name='blogtags', to='general_settings.skill', verbose_name='Blog Tags'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='created_by',
            field=models.ForeignKey(help_text='This blog will be removed if author is deleted', on_delete=django.db.models.deletion.CASCADE, related_name='announcer', to=settings.AUTH_USER_MODEL, verbose_name='Publisher'),
        ),
    ]
