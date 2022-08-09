# Generated by Django 3.2.8 on 2022-07-24 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0007_payday'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payday',
            options={'verbose_name': 'Payday', 'verbose_name_plural': 'Payday'},
        ),
        migrations.RemoveField(
            model_name='payday',
            name='duration',
        ),
        migrations.AddField(
            model_name='payday',
            name='preview',
            field=models.CharField(choices=[('one_day', '01 Day'), ('two_days', '02 Days'), ('three_days', '03 Days'), ('four_days', '04 Days'), ('five_days', '05 Days'), ('six_days', '06 Days'), ('one_week', '01 Week'), ('two_weeks', '02 Weeks'), ('three_weeks', '03 Weeks'), ('one_month', '01 Month')], default='three_days', help_text='"01 Week" means 7 Days, "02 Weeks" means 14 Days, "03 Weeks" means 21 Days, "01 Month" means 28-30 Days', max_length=20, verbose_name='Preview'),
        ),
    ]