# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-07 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoja_ruta', '0004_auto_20181106_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='hojaruta',
            name='altura_desde',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='hojaruta',
            name='altura_hasta',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='hojaruta',
            name='cant_registros',
            field=models.IntegerField(default=0),
        ),
    ]
