# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0005_auto_20170409_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre_logo',
            field=models.ImageField(default='readers/no_image.png', upload_to=b''),
        ),
    ]
