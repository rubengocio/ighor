# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-28 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0005_barrio_codigo_postal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provincia',
            name='nombre',
            field=models.CharField(db_index=True, max_length=127),
        ),
    ]