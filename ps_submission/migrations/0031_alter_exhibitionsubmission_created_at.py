# Generated by Django 4.2.9 on 2024-09-08 08:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ps_submission", "0030_alter_exhibitionsubmission_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exhibitionsubmission",
            name="created_at",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 9, 8, 8, 12, 24, 221339, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Created",
            ),
        ),
    ]
