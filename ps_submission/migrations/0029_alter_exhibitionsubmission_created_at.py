# Generated by Django 4.2.9 on 2024-06-30 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_submission', '0028_exhibitionsubmission_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2024, 6, 30, 8, 57, 40, 761769, tzinfo=datetime.timezone.utc), verbose_name='Created'),
        ),
    ]
