# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
from normalizador.enum import ESTADO_CHOICES, ACTIVO, INACTIVO
from normalizador.models.localidad import Localidad


class Cuadrante(models.Model):
    nombre = models.CharField(max_length=127)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)

    class Meta:
        unique_together = (("nombre", "localidad"),)

    def __str__(self):
        return u"%s" % self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre