# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-23 01:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0016_diccionariobarrio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criterio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=127)),
                ('valor', models.CharField(max_length=127)),
            ],
        ),
    ]
