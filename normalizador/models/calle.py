# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
from normalizador.enum import ESTADO_CHOICES, ACTIVO


class Calle(models.Model):
    nombre = models.CharField(max_length=127, db_index=True)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)

    def __str__(self):
        return u"%s" % self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre

