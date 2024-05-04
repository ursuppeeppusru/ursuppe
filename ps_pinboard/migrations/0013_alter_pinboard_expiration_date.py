# Generated by Django 4.2.10 on 2024-05-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ps_pinboard', '0012_pinboard_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pinboard',
            name='expiration_date',
            field=models.DateField(help_text='Required *. The post will be removed after the expiration date<br/><br/>e.g., 14/10/2023', null=True, verbose_name='Expiration date'),
        ),
    ]
