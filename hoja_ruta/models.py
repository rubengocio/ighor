# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio


class NumeroHojarRuta(models.Model):
    numero=models.IntegerField(default=0)

    def __str__(self):
        return u'%d' % self.numero

    def __unicode__(self):
        return u'%d' % self.numero


class HistorialHojaRuta(models.Model):
    fecha=models.DateTimeField(auto_now_add=True)
    barrio=models.ForeignKey(Barrio, null=True, blank=True)
    owner=models.ForeignKey(User)

    def __str__(self):
        return self.fecha.strftime("%d/%m/%Y")


class HojaRuta(models.Model):
    SIN_ASIGNAR=1
    ASIGNADA=2
    CON_DEVOLUCION=3
    CHOICES_ESTADO=(
        (SIN_ASIGNAR, u'Sin Asignar'),
        (ASIGNADA, u'Asignada'),
        (CON_DEVOLUCION, u'Cerrada')
    )


    historial=models.ForeignKey(HistorialHojaRuta, related_name='hojas_ruta')
    numero = models.CharField(max_length=8, db_index=True)
    calle_barrio = models.ForeignKey(CallesBarrio)
    altura_desde = models.CharField(max_length=10, blank=True, null=True)
    altura_hasta = models.CharField(max_length=10, blank=True, null=True)
    cant_registros = models.IntegerField(default=0)
    asignada_a=models.ForeignKey(User, null=True, blank=True)
    estado=models.IntegerField(choices=CHOICES_ESTADO, default=SIN_ASIGNAR)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s - %s" % (self.historial, self.numero)

    def __unicode__(self):
        return u"%s - %s" % (self.historial, self.numero)

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


    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.asignada_a and self.estado==HojaRuta.SIN_ASIGNAR:
            self.estado=HojaRuta.ASIGNADA

        super(HojaRuta, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)



class DetalleHojaRuta(models.Model):
    hoja_ruta=models.ForeignKey(HojaRuta)
    numero_orden=models.CharField(max_length=2)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u'%s' % self.id


