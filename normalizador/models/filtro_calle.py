# -*- coding: utf-8 -*-
from django.db import models

from normalizador.constants import CHOICES_OPERATOR
from normalizador.models import Criterio
from normalizador.models.calles_barrio import CallesBarrio


class FiltroCalle(models.Model):
    calle_barrio=models.ForeignKey(CallesBarrio)
    operador=models.IntegerField(choices=CHOICES_OPERATOR)
    parentesis_abierto=models.BooleanField(default=False)
    criterio=models.ForeignKey(Criterio, blank=True, null=True)
    valor=models.CharField(max_length=255)
    parentesis_cerrado=models.BooleanField(default=False)