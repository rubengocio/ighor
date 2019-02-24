# -*- coding: utf-8 -*-
from django.db import models, connection

# Create your models here.
from normalizador.enum import ESTADO_CHOICES, ACTIVO, INACTIVO
from normalizador.models.provincia import Provincia


class Localidad(models.Model):
    nombre = models.CharField(max_length=127, db_index=True)
    codigo_postal = models.CharField(max_length=10)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)

    def __str__(self):
        return u"%s" % self.nombre

    def __unicode__(self):
        return u"%s" % self.nombre

    @staticmethod
    def quitar_espacios():
        exito = True
        try:
            query = ' UPDATE normalizador_localidad SET nombre = UPPER(TRIM(nombre)) '
            cursor = connection.cursor()
            cursor.cursor.execute(query)

        except Exception as ex:
            print(ex)
            exito = False
        finally:
            cursor.cursor.close()
        return exito
