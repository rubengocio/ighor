# -*- coding: utf-8 -*-
from django.db import models


class Titular(models.Model):
    estado = models.CharField(max_length=5, blank=True, null=True, default=None)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    descripcion = models.CharField(max_length=255, blank=True, null=True, default=None)
    titular = models.IntegerField(blank=True, null=True, default=0)
    apellido = models.CharField(max_length=255, blank=True, null=True, default=None)
    nombre = models.CharField(max_length=255, blank=True, null=True, default=None)
    numero = models.IntegerField(blank=True, null=True, default=None)
    piso = models.CharField(max_length=255, blank=True, null=True, default=None)
    depto = models.CharField(max_length=255, blank=True, null=True, default=None)
    barrio = models.CharField(max_length=255, blank=True, null=True, default=None)
    telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    localidad = models.CharField(max_length=255, blank=True, null=True, default=None)
    lp = models.CharField(max_length=255, blank=True, null=True, default=None)
    provincia = models.CharField(max_length=255, blank=True, null=True, default=None)
    empresas = models.CharField(max_length=255, blank=True, null=True, default=None)
    telefono_alternativo = models.CharField(max_length=255, blank=True, null=True, default=None)
    sexo = models.CharField(max_length=255, blank=True, null=True, default=None)
    fecha_nacimiento = models.IntegerField(blank=True, null=True, default=None)
    fecha_alta = models.IntegerField(blank=True, null=True, default=None)
    tipo_cuenta = models.CharField(max_length=1, blank=True, null=True, default=None)

