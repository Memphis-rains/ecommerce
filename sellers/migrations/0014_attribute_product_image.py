# Generated by Django 2.2.14 on 2024-01-30 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0013_remove_attribute_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='product_image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
