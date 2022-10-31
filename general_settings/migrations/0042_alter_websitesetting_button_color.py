# Generated by Django 3.2.8 on 2022-10-27 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_settings', '0041_remove_websitesetting_embed_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='websitesetting',
            name='button_color',
            field=models.CharField(blank=True, default='purple', help_text="Customize colors for signup, login, any other visitor buttons. Example '3F0F8FF', or 'red' or 'blue' or 'purple' or any css color code. Warning!: Donnot add quotation marks around the color attributes", max_length=100, null=True, verbose_name='Visitor Buttons'),
        ),
    ]
