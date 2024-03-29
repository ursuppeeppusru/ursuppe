# Generated by Django 4.2.9 on 2024-03-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_calendar', '0018_alter_calendarsubmission_opening_hours_for_opening_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarsubmission',
            name='artists',
            field=models.TextField(help_text='Required *<br/><br/>Divide multiple artists with comma (,)', verbose_name='Artist(s)'),
        ),
        migrations.AlterField(
            model_name='calendarsubmission',
            name='event_type',
            field=models.CharField(choices=[('Exhibition', 'Exhibition'), ('Performance', 'Performance'), ('Screening', 'Screening'), ('Fundraiser', 'Fundraiser'), ('Other', 'Other')], default='Exhibition', help_text='Required *', max_length=500, verbose_name='Type'),
        ),
    ]
