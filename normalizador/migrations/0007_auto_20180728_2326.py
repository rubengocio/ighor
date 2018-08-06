# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-28 23:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0006_auto_20180728_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barrio',
            name='nombre',
            field=models.CharField(db_index=True, max_length=127),
        ),
        migrations.AlterField(
            model_name='localidad',
            name='nombre',
            field=models.CharField(db_index=True, max_length=127),
        ),
        migrations.AlterUniqueTogether(
            name='barrio',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='cuadrante',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='localidad',
            unique_together=set([]),
        ),
    ]