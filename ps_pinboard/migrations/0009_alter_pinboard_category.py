# Generated by Django 4.2.9 on 2024-03-06 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_pinboard', '0008_alter_pinboard_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinboard',
            name='category',
            field=models.CharField(choices=[('open-call', 'Open call'), ('news', 'News'), ('education', 'Education'), ('residency', 'Residency'), ('job', 'Job'), ('funding', 'Funding'), ('studio', 'Studio'), ('trade', 'Trade'), ('other', 'Other')], default='Exhibition', help_text='Required *', max_length=500, verbose_name='Category'),
        ),
    ]
