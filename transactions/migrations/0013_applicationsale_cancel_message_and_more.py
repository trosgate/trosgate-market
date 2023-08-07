# Generated by Django 4.1.9 on 2023-08-05 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0012_alter_applicationsale_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationsale',
            name='cancel_message',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message'),
        ),
        migrations.AddField(
            model_name='applicationsale',
            name='cancel_status',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('approved', 'Approved')], max_length=100, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='applicationsale',
            name='cancel_type',
            field=models.CharField(blank=True, choices=[('not_cancelled', 'No cancellation requested'), ('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type'),
        ),
        migrations.AddField(
            model_name='applicationsale',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On'),
        ),
        migrations.AddField(
            model_name='contractsale',
            name='cancel_message',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message'),
        ),
        migrations.AddField(
            model_name='contractsale',
            name='cancel_status',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('approved', 'Approved')], max_length=100, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='contractsale',
            name='cancel_type',
            field=models.CharField(blank=True, choices=[('not_cancelled', 'No cancellation requested'), ('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type'),
        ),
        migrations.AddField(
            model_name='contractsale',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On'),
        ),
        migrations.AddField(
            model_name='extcontract',
            name='cancel_message',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message'),
        ),
        migrations.AddField(
            model_name='extcontract',
            name='cancel_status',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('approved', 'Approved')], max_length=100, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='extcontract',
            name='cancel_type',
            field=models.CharField(blank=True, choices=[('not_cancelled', 'No cancellation requested'), ('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type'),
        ),
        migrations.AddField(
            model_name='extcontract',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On'),
        ),
        migrations.AddField(
            model_name='proposalsale',
            name='cancel_message',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Additional Message'),
        ),
        migrations.AddField(
            model_name='proposalsale',
            name='cancel_status',
            field=models.CharField(blank=True, choices=[('initiated', 'Initiated'), ('approved', 'Approved')], max_length=100, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='proposalsale',
            name='cancel_type',
            field=models.CharField(blank=True, choices=[('not_cancelled', 'No cancellation requested'), ('deadline_exceeded', 'Deadline Exceeded'), ('user_abandoned_work', 'Work Abandoned'), ('user_not_responding', 'Client not Responding to Chat'), ('user_is_abusive', 'User is Abusive'), ('ordered_wrong_product', 'Wrong Product Ordered'), ('different_product_delivered', 'A different service/product submitted')], max_length=100, null=True, verbose_name='Issue Type'),
        ),
        migrations.AddField(
            model_name='proposalsale',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Cancelled On'),
        ),
        migrations.AlterField(
            model_name='applicationsale',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='pending', max_length=20, verbose_name='Action Type'),
        ),
        migrations.AlterField(
            model_name='contractsale',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='pending', max_length=20, verbose_name='Action Type'),
        ),
        migrations.AlterField(
            model_name='extcontract',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='pending', max_length=20, verbose_name='Action Type'),
        ),
        migrations.AlterField(
            model_name='proposalsale',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('approved', 'Approved')], default='pending', max_length=20, verbose_name='Action Type'),
        ),
    ]
