# Generated by Django 2.2.14 on 2024-01-24 10:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0004_auto_20240124_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])]),
        ),
    ]
