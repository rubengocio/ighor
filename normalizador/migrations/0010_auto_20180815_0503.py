# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-15 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0009_auto_20180808_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localidad',
            name='codigo_postal',
            field=models.CharField(max_length=10),
        ),
    ]
