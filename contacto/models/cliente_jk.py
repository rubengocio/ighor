# -*- coding: utf-8 -*-
from django.db import models


class ClienteJK(models.Model):
    cod_cliente = models.CharField(max_length=255, blank=True, null=True, default=None)
    nombre = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    tipo_documento = models.IntegerField(blank=True, null=True, default=None, db_index=True)
    nro_documento = models.IntegerField(blank=True, null=True, default=None, db_index=True)
    telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    calle = models.CharField(max_length=255, blank=True, null=True, default=None)
    numero = models.CharField(max_length=255, blank=True, null=True, default=None)
    barrio = models.CharField(max_length=255, blank=True, null=True, default=None)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    cuadrante = models.CharField(max_length=255, blank=True, null=True, default=None)
    cualidad = models.CharField(max_length=255, blank=True, null=True, default=None)
    inhumados = models.CharField(max_length=255, blank=True, null=True, default=None)
    productos = models.CharField(max_length=255, blank=True, null=True, default=None)
    meses_deuda = models.CharField(max_length=255, blank=True, null=True, default=None)
    monto_deuda = models.CharField(max_length=255, blank=True, null=True, default=None)
    tel_naranja = models.CharField(max_length=255, blank=True, null=True, default=None)
    tel_jakemate_1 = models.CharField(max_length=255, blank=True, null=True, default=None)
    tel_jakemate_2 = models.CharField(max_length=255, blank=True, null=True, default=None)
    tel_jakemate_3 = models.CharField(max_length=255, blank=True, null=True, default=None)
    ultimo_pago= models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Cliente JakeMate'
        verbose_name_plural = 'Clientes JakeMate'

