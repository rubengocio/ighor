# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-26 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0025_auto_20180826_0835'),
        ('contacto', '0008_auto_20180826_0042'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactonormalizado',
            name='localidad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='normalizador.Localidad'),
        ),
    ]
