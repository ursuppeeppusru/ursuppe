# Generated by Django 4.2.7 on 2024-01-30 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_calendar', '0014_alter_calendarsubmission_location_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarsubmission',
            name='link_to_location',
            field=models.URLField(blank=True, help_text='URL e.g., https://ladder.dk', verbose_name='Location link/URL'),
        ),
        migrations.AlterField(
            model_name='calendarsubmission',
            name='location',
            field=models.CharField(help_text='Required *', max_length=255, verbose_name='Location name'),
        ),
    ]
