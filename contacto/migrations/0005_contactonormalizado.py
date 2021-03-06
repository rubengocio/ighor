# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-25 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('normalizador', '0024_auto_20180825_0115'),
        ('contacto', '0004_auto_20180824_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactoNormalizado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(blank=True, db_index=True, default=0, null=True)),
                ('titular', models.IntegerField(blank=True, db_index=True, default=0, null=True)),
                ('apellido', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('nombre', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('altura', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('piso', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('departamento', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('observaciones', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('estado', models.IntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], db_index=True, default=1)),
                ('fecha_actualizacion', models.DateTimeField()),
                ('barrio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='normalizador.Barrio')),
                ('calle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='normalizador.Calle')),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='normalizador.Provincia')),
            ],
        ),
    ]
