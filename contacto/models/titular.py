# -*- coding: utf-8 -*-
from django.db import models


class Titular(models.Model):
    estado = models.CharField(max_length=5, blank=True, null=True, default=None)
    tipo = models.IntegerField(blank=True, null=True, default=0, db_index=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True, default=None)
    titular = models.IntegerField(blank=True, null=True, default=0, db_index=True)
    apellido = models.CharField(max_length=255, blank=True, null=True, default=None)
    nombre = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_calle = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_numero = models.IntegerField(blank=True, null=True, default=None)
    domicilio_piso = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_depto = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_barrio = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    localidad = models.CharField(max_length=255, blank=True, null=True, default=None)
    lp = models.CharField(max_length=255, blank=True, null=True, default=None)
    provincia = models.CharField(max_length=255, blank=True, null=True, default=None)
    empresas = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_calle = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_numero = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_piso = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_depto = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_barrio = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_localidad = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_lp = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_provincia = models.CharField(max_length=255, blank=True, null=True, default=None)
    telefono_alternativo = models.CharField(max_length=255, blank=True, null=True, default=None)
    sexo = models.CharField(max_length=255, blank=True, null=True, default=None)
    fecha_nacimiento = models.IntegerField(blank=True, null=True, default=None)
    fecha_alta = models.IntegerField(blank=True, null=True, default=None)
    tipo_cuenta = models.CharField(max_length=1, blank=True, null=True, default=None)


