# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-15 05:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0011_titular'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Titular',
        ),
    ]
