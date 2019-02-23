# -*- coding: utf-8 -*-
from django.db import models

from normalizador.models.calle_incorrecta import CalleIncorrecta
from normalizador.models.calles_barrio import CallesBarrio


class DiccionarioCalle(models.Model):
    calle_incorrecta = models.ForeignKey(CalleIncorrecta)
    calle_barrio = models.ForeignKey(CallesBarrio)

    class Meta:
        unique_together = (("calle_incorrecta", "calle_barrio"),)
