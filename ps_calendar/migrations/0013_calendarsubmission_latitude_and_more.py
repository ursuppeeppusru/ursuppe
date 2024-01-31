# Generated by Django 4.2.7 on 2024-01-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_calendar', '0012_calendarsubmission_event_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarsubmission',
            name='latitude',
            field=models.DecimalField(decimal_places=10, max_digits=18, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='calendarsubmission',
            name='longitude',
            field=models.DecimalField(decimal_places=10, max_digits=18, null=True, verbose_name='Longitude'),
        ),
    ]
