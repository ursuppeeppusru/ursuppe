# Generated by Django 4.2.9 on 2024-06-30 08:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ps_submission', '0027_alter_exhibitionimages_cover_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibitionsubmission',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
    ]