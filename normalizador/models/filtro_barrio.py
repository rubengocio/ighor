# -*- coding: utf-8 -*-
from django.db import models

from normalizador.models import Criterio
from normalizador.models.barrio import Barrio

OR=0
AND=1
CHOICES_OPERATOR=(
    (OR, 'OR'),
    (AND, 'AND')
)

class FiltroBarrio(models.Model):
    barrio=models.ForeignKey(Barrio)
    operador=models.IntegerField(choices=CHOICES_OPERATOR)
    parentesis_abierto=models.BooleanField(default=False)
    criterio=models.ForeignKey(Criterio, blank=True, null=True)
    valor=models.CharField(max_length=255)
    parentesis_cerrado=models.BooleanField(default=False)