# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-07 01:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hoja_ruta', '0006_auto_20181107_0134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hojaruta',
            old_name='asiganda_a',
            new_name='asignada_a',
        ),
    ]