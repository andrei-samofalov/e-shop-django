# Generated by Django 4.2 on 2023-04-20 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sitesettings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='datetime_format',
            field=models.CharField(choices=[('%m/%d/%Y', 'mm/dd/yyyy'), ('%H:%M %d.%m.%Y', 'HH:MM mm.dd.yyyy')], help_text='choose datetime format that will be represented through entire project', verbose_name='datetime formats'),
        ),
    ]
