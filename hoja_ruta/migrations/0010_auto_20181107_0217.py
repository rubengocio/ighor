# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-07 02:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hoja_ruta', '0009_historialhojaruta_barrio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialhojaruta',
            name='barrio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='normalizador.Barrio'),
        ),
    ]