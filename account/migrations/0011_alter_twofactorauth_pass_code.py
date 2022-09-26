# Generated by Django 3.2.8 on 2022-09-01 19:59

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_customer_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twofactorauth',
            name='pass_code',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=255, null=True, verbose_name='Access Token')),
        ),
    ]