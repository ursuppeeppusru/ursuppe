# Generated by Django 4.2.9 on 2024-03-06 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_submission', '0019_exhibitionimages_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='description',
            field=models.TextField(help_text='Required *', verbose_name='Text/description/press release'),
        ),
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='exhibition_end',
            field=models.DateField(help_text='Required*<br/><br/>e.g., 16/10/2023', verbose_name='Exhibition end'),
        ),
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='exhibition_opening',
            field=models.DateField(help_text='Required*<br/><br/>e.g., 14/10/2023', verbose_name='Exhibition opening'),
        ),
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='link_to_video',
            field=models.URLField(blank=True, verbose_name='Link to video'),
        ),
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='social_media_info',
            field=models.TextField(blank=True, verbose_name='Social media info'),
        ),
        migrations.AlterField(
            model_name='exhibitionsubmission',
            name='text_author',
            field=models.CharField(help_text='Required *', max_length=255, verbose_name='Text author'),
        ),
    ]
