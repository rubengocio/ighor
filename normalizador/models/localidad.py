# -*- coding: utf-8 -*-
from django.db import models



# Create your models here.
from normalizador.enum import ESTADO_CHOICES, ACTIVO, INACTIVO
from normalizador.models.provincia import Provincia


class Localidad(models.Model):
    nombre = models.CharField(max_length=127)
    codigo_postal = models.CharField(max_length=5)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)

    class Meta:
        unique_together = (("nombre", "provincia"),)

    def __str__(self):
        return u"%s" % self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre
