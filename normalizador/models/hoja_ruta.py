# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
from normalizador.models.barrio import Barrio


class HojaRuta(models.Model):
    numero_hoja = models.CharField(max_length=8, db_index=True)
    barrio = models.ForeignKey(Barrio)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.numero_hoja

    def __unicode__(self):
        return u"%s" % self.numero_hoja


class DetalleHojaRuta(models.Model):
    hoja_ruta=models.ForeignKey(HojaRuta)
    numero_orden=models.CharField(max_length=2)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return u'%s - %s' % (self.hoja_ruta.numero_hoja, self.numero_orden)

    def __unicode__(self):
        return u'%s - %s' % (self.hoja_ruta.numero_hoja, self.numero_orden)