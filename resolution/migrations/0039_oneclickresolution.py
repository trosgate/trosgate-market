# Generated by Django 3.2.8 on 2022-08-27 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0014_alter_oneclickpurchase_options'),
        ('teams', '0013_alter_package_monthly_projects_applicable_per_team'),
        ('resolution', '0038_contractcompletionfiles'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneClickResolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start Time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End Time')),
                ('status', models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')], default='ongoing', max_length=20, verbose_name='Action Type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('oneclick_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oneclickaction', to='transactions.oneclickpurchase', verbose_name='One Click Product')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paidoneclickteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'verbose_name': 'One Click Hired',
                'verbose_name_plural': 'One Click Hired',
                'ordering': ('-created_at',),
            },
        ),
    ]
