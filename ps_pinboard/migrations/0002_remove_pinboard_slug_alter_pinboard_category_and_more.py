# Generated by Django 4.2.9 on 2024-03-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_pinboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pinboard',
            name='slug',
        ),
        migrations.AlterField(
            model_name='pinboard',
            name='category',
            field=models.CharField(choices=[('Open call', 'Open call'), ('News', 'News'), ('Course and education', 'Courses and education'), ('Residency', 'Residency'), ('Job', 'Job'), ('Funding or grant', 'Funding or grant'), ('Atelier/studio', 'Atelier/studio'), ('Trade (buying/selling)', 'Trade (buying/selling)'), ('Other', 'Other')], default='Exhibition', help_text='Required *', max_length=500, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='pinboard',
            name='consent_to_collect_info',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], help_text='Required *', verbose_name='Do you consent to having collected and expose your contact information?'),
        ),
    ]
