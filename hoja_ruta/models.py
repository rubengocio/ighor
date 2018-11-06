# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.
from normalizador.models.calles_barrio import CallesBarrio


class NumeroHojarRuta(models.Model):
    numero=models.IntegerField(default=0)

    def __str__(self):
        return u'%d' % self.numero

    def __unicode__(self):
        return u'%d' % self.numero


class HojaRuta(models.Model):
    numero = models.CharField(max_length=8, db_index=True)
    calle_barrio = models.ForeignKey(CallesBarrio)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.numero

    def __unicode__(self):
        return u"%s" % self.numero

    @staticmethod
    def nextNumber():
        object = NumeroHojarRuta.objects.all().first()
        if object is None:
            object = NumeroHojarRuta()
        object.numero += 1
        object.save()
        return object.numero

    @staticmethod
    def currentNumber():
        object = NumeroHojarRuta.objects.all().first()
        if object is None:
            object = NumeroHojarRuta()
        return object.numero


class DetalleHojaRuta(models.Model):
    hoja_ruta=models.ForeignKey(HojaRuta)
    numero_orden=models.CharField(max_length=2)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u'%s' % self.id