# Generated by Django 4.2.5 on 2024-01-16 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_calendar', '0003_alter_calendarimages_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarimages',
            name='caption',
            field=models.CharField(help_text='Caption for the image', max_length=255, verbose_name='Image Caption'),
        ),
        migrations.AlterField(
            model_name='calendarsubmission',
            name='exhibition_end',
            field=models.DateField(help_text='eg. 2024-01-02 Required*', verbose_name='Exhibition End'),
        ),
        migrations.AlterField(
            model_name='calendarsubmission',
            name='exhibition_opening',
            field=models.DateField(help_text='eg. 2024-01-01  Required*', verbose_name='Exhibition Opening'),
        ),
    ]
