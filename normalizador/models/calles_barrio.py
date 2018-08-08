# -*- coding: utf-8 -*-
from django.db import models

from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle


class CallesBarrio(models.Model):
    barrio = models.ForeignKey(Barrio)
    calle = models.ForeignKey(Calle)
    altura_desde = models.PositiveIntegerField(null=True, blank=True, default=None)
    altura_hasta = models.PositiveIntegerField(null=True, blank=True, default=None)
    referencia = models.CharField(max_length=127, null=True, blank=True, default=None)
    plano=models.CharField(max_length=127, null=True, blank=True, default=None)
    ubicacion=models.CharField(max_length=127, null=True, blank=True, default=None)
    nomenclado=models.BooleanField(default=False)

    class Meta:
        unique_together = (("barrio", "calle"),)

    def __str__(self):
        return u"%s - %s" % (self.barrio.nombre, self.calle.nombre)

    def __unicode__(self):
        return u"%s - %s" % (self.barrio.nombre, self.calle.nombre)