# -*- coding: utf-8 -*-
from django.db import models

from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle


class CallesBarrio(models.Model):
    PAIR=1
    ODD=2
    ALL=3
    CHOICES_TYPE_NUMBER=(
        (PAIR,'Par'),
        (ODD, 'Impar'),
        (ALL, 'Todas las numeraciones')
    )

    barrio = models.ForeignKey(Barrio)
    calle = models.ForeignKey(Calle)
    altura_desde = models.PositiveIntegerField(null=True, blank=True, default=None)
    altura_hasta = models.PositiveIntegerField(null=True, blank=True, default=None)
    referencia = models.CharField(max_length=127, null=True, blank=True, default=None)
    plano = models.CharField(max_length=127, null=True, blank=True, default=None)
    ubicacion = models.CharField(max_length=127, null=True, blank=True, default=None)
    tipo_numeracion = models.IntegerField(choices=CHOICES_TYPE_NUMBER, default=ALL, db_index=True)
    nomenclado = models.BooleanField(default=False)


    class Meta:
        unique_together = (("barrio", "calle"),)

    def __str__(self):
        return u"%s - %s" % (self.barrio.nombre, self.calle.nombre)

    def __unicode__(self):
        return u"%s - %s" % (self.barrio.nombre, self.calle.nombre)