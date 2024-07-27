# Generated by Django 4.2.9 on 2024-07-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_pinboard', '0014_alter_pinboard_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinboard',
            name='category',
            field=models.CharField(choices=[('open call', 'Open call'), ('news', 'News'), ('education', 'Education'), ('residency', 'Residency'), ('job', 'Job'), ('funding', 'Funding'), ('studio', 'Studio'), ('trade', 'Trade'), ('other', 'Other')], default='Exhibition', help_text='Required *', max_length=500, verbose_name='Category'),
        ),
    ]
