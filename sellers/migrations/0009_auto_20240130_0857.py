# Generated by Django 2.2.14 on 2024-01-30 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0008_auto_20240130_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]