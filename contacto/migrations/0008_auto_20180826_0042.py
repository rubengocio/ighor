# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-26 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0007_auto_20180825_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titular',
            name='domicilio_calle',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='titular',
            name='localidad',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='titular',
            name='provincia',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=255, null=True),
        ),
    ]
