# Generated by Django 2.2.14 on 2024-01-25 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0005_auto_20240124_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]
