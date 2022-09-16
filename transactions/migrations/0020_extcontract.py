# Generated by Django 3.2.8 on 2022-09-16 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0020_alter_assignmember_options'),
        ('contract', '0019_auto_20220908_2342'),
        ('transactions', '0019_alter_purchase_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.PositiveIntegerField(verbose_name='Sales Price')),
                ('total_sales_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Contract Total')),
                ('disc_sales_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Discounted Salary')),
                ('staff_hired', models.PositiveIntegerField(default=1, verbose_name='Staff Hired')),
                ('earning_fee_charged', models.PositiveIntegerField(verbose_name='Earning Fee')),
                ('total_earning_fee_charged', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total Earning Fee')),
                ('earning', models.PositiveIntegerField(verbose_name='Earning')),
                ('total_earning', models.PositiveIntegerField(blank=True, null=True, verbose_name='Total Earning')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ordered On')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified On')),
                ('is_refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontracthired', to='contract.contract', verbose_name='Contract Hired')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extcontractsales', to='transactions.purchase', verbose_name='Purchase Client')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hiredextcontractteam', to='teams.team', verbose_name='Team')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
