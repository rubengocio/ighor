# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import OuterRef
from django.db.models import Subquery

from contacto.models import ContactoNormalizado
from contacto.models.cliente_jk import ClienteJK
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
    DEVOLUCION_INCOMPLETA=4

    CHOICES_ESTADO=(
        (SIN_ASIGNAR, u'Sin Asignar'),
        (ASIGNADA, u'Asignada'),
        (CON_DEVOLUCION, u'Cerrada'),
        (DEVOLUCION_INCOMPLETA, u'Devolucion Incompleta')
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

    def update_status(self):

        detalles_hojas=DetalleHojaRuta.objects.filter(hoja_ruta=self)
        total_rows=detalles_hojas.count()
        cant_completas=0

        for detalle in detalles_hojas:
            if detalle.is_completa:
                cant_completas +=1

        if cant_completas > 1 and cant_completas != total_rows:
            self.estado=HojaRuta.DEVOLUCION_INCOMPLETA
            self.save()

        if cant_completas == total_rows:
            self.estado = HojaRuta.CON_DEVOLUCION
            self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.asignada_a and self.estado==HojaRuta.SIN_ASIGNAR:
            self.estado=HojaRuta.ASIGNADA

        super(HojaRuta, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)


class Observacion(models.Model):
    nombre=models.CharField(max_length=125, unique=True)

    def __str__(self):
        return u'%s' % self.nombre

    def __unicode__(self):
        return u'%s' % self.nombre


class Producto(models.Model):
    nombre=models.CharField(max_length=125, unique=True)

    def __str__(self):
        return u'%s' % self.nombre

    def __unicode__(self):
        return u'%s' % self.nombre


class DetalleHojaRuta(models.Model):
    hoja_ruta = models.ForeignKey(HojaRuta, related_name='detalle_hoja_ruta')
    numero_orden = models.CharField(max_length=2)
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)
    observacion = models.ForeignKey(Observacion, null=True, blank=True)
    is_completa = models.BooleanField(default=False)

    contact = None
    cliente_jk = None

    def __str__(self):
        return u'%s' % self.id

    def __unicode__(self):
        return u'%s' % self.id


    @property
    def apellido(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.apellido if self.contact else ''

    @property
    def nombre(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.nombre if self.contact else ''

    @property
    def provincia(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.provincia if self.contact else ''

    @property
    def localidad(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.localidad if self.contact else ''

    @property
    def barrio(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.barrio if self.contact else ''

    @property
    def calle(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.calle if self.contact else ''

    @property
    def altura(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.altura if self.contact else ''

    @property
    def piso(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.piso if self.contact else ''

    @property
    def departamento(self):
        if self.contact is None:
            self.contact = ContactoNormalizado.objects.filter(tipo=self.tipo, titular=self.titular).first()
        return self.contact.departamento if self.contact else ''

    @property
    def telefono(self):
        if self.cliente_jk is None:
            self.cliente_jk = ClienteJK.objects.filter(tipo_documento=self.tipo, nro_documento=self.titular).first()
        return (self.cliente_jk.telefono if self.cliente_jk.telefono == '0' else '') if self.cliente_jk else ''

    @property
    def deuda(self):
        if self.cliente_jk is None:
            self.cliente_jk = ClienteJK.objects.filter(tipo_documento=self.tipo, nro_documento=self.titular).first()
        return ('Si' if len(self.cliente_jk.monto_deuda) > 0 else 'No') if self.cliente_jk else ''

    @property
    def productos(self):
        if self.cliente_jk is None:
            self.cliente_jk = ClienteJK.objects.filter(tipo_documento=self.tipo, nro_documento=self.titular).first()
        return (self.cliente_jk.productos if self.cliente_jk.productos != 'NULL' else '') if self.cliente_jk else ''

    @property
    def inhumados(self):
        if self.cliente_jk is None:
            self.cliente_jk = ClienteJK.objects.filter(tipo_documento=self.tipo, nro_documento=self.titular).first()
        return (self.cliente_jk.inhumados if self.cliente_jk.inhumados != 'NULL' else 'No') if self.cliente_jk else ''

    @property
    def activos(self):
        if self.cliente_jk is None:
            self.cliente_jk = ClienteJK.objects.filter(tipo_documento=self.tipo, nro_documento=self.titular).first()
        return 'Si'

    @property
    def observaciones(self):
        detalle=DetalleHojaRuta.objects.filter(tipo=self.tipo, titular=self.titular, observacion__isnull=False).last()
        return detalle.observacion.nombre if detalle else ''

    def save(self, *args, **kwargs):

        self.is_completa = True if self.observacion or self.detalle_productos.count() > 0 else False

        super(DetalleHojaRuta, self).save(*args, **kwargs)

        self.hoja_ruta.update_status()


class ProductosDetalleHojaRuta(models.Model):
    detalle = models.ForeignKey(DetalleHojaRuta, related_name='detalle_productos')
    producto = models.ManyToManyField(Producto, blank=True)