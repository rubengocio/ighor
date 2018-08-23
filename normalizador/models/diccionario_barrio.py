# -*- coding: utf-8 -*-
from django.db import models

from normalizador.models.barrio import Barrio


class DiccionarioBarrio(models.Model):
    nombre=models.CharField(max_length=50, db_index=True)
    barrio=models.ForeignKey(Barrio, blank=True, null=True)
    actualizado=models.BooleanField(default=False, db_index=True)
