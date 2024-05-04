# Generated by Django 4.2.10 on 2024-05-04 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_submission', '0025_alter_exhibitionsubmission_curators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='curators',
            field=models.CharField(blank=True, help_text='Divide multiple curators with comma (,)', max_length=255, verbose_name='Curator(s)'),
        ),
    ]