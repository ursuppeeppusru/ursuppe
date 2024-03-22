# Generated by Django 4.2.9 on 2024-03-06 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_pinboard', '0006_alter_pinboard_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinboard',
            name='category',
            field=models.CharField(choices=[('Open call', 'Open call'), ('news', 'News'), ('education', 'Courses and education'), ('residency', 'Residency'), ('job', 'Job'), ('funding', 'Funding or grant'), ('studio', 'Atelier/studio'), ('trade', 'Trade (buying/selling)'), ('other', 'Other')], default='Exhibition', help_text='Required *', max_length=500, verbose_name='Category'),
        ),
    ]
