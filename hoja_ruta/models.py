# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from contacto.models import ContactoNormalizado
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

    @property
    def vendedor(self):
        if self.asignada_a:
            return u'%s, %s' % (self.asignada_a.last_name, self.asignada_a.first_name)
        else:
            return u'No Asignado'

    @property
    def numero_hoja_ruta(self):
        return self.numero.rjust(8, '0')

    @property
    def detalles(self):
        return self.detalle_hoja_ruta.all()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.asignada_a and self.estado==HojaRuta.SIN_ASIGNAR:
            self.estado=HojaRuta.ASIGNADA

        super(HojaRuta, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)



class DetalleHojaRuta(models.Model):
    hoja_ruta=models.ForeignKey(HojaRuta, related_name='detalle_hoja_ruta')
    numero_orden=models.CharField(max_length=2)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)

    contact=None
    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u'%s' % self.id

    @property
    def apellido(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.apellido

    @property
    def nombre(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.nombre

    @property
    def provincia(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.provincia

    @property
    def localidad(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.localidad

    @property
    def barrio(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.barrio

    @property
    def calle(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.calle

    @property
    def altura(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.altura

    @property
    def piso(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.piso

    @property
    def departamento(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.departamento

    @property
    def observaciones(self):
        if self.contact is None:
            self.contact=ContactoNormalizado.objects.get(tipo=self.tipo, titular=self.titular)
        return self.contact.observaciones



