# -*- coding: utf-8 -*-
from django.db import models, connection

# Create your models here.
from normalizador.enum import ESTADO_CHOICES, ACTIVO, INACTIVO
from normalizador.models.cuadrante import Cuadrante


class Barrio(models.Model):
    nombre = models.CharField(max_length=127, db_index=True)
    codigo_postal = models.CharField(max_length=10)
    cuadrante = models.ForeignKey(Cuadrante, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)

    def __str__(self):
        return u"%s" % self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre

    @staticmethod
    def quitar_espacios():
        try:
            query = ' UPDATE normalizador_provincia SET nombre = UPPER(TRIM(nombre)) '
            cursor = connection.cursor()
            cursor.execute(query)

        except Exception as ex:
            print(ex)
            return False
        return True
