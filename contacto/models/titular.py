# -*- coding: utf-8 -*-
from django.db import models, connection

from contacto import commons
from contacto.models import ContactoNormalizado


class Titular(models.Model):
    estado = models.CharField(max_length=5, blank=True, null=True, default=None)
    tipo = models.IntegerField(blank=True, null=True, default=commons.DNI, db_index=True, choices=commons.TIPO_DOCUMENTO_CHOICES)
    descripcion = models.CharField(max_length=255, blank=True, null=True, default=None)
    titular = models.IntegerField(blank=True, null=True, default=0, db_index=True)
    apellido = models.CharField(max_length=255, blank=True, null=True, default=None)
    nombre = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_calle = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    domicilio_numero = models.IntegerField(blank=True, null=True, default=None)
    domicilio_piso = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_depto = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_barrio = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    localidad = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    lp = models.CharField(max_length=255, blank=True, null=True, default=None)
    provincia = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    empresas = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_calle = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_numero = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_piso = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_depto = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_barrio = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_telefono = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_codigo_postal = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_localidad = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_lp = models.CharField(max_length=255, blank=True, null=True, default=None)
    domicilio_laboral_provincia = models.CharField(max_length=255, blank=True, null=True, default=None)
    telefono_alternativo = models.CharField(max_length=255, blank=True, null=True, default=None)
    sexo = models.CharField(max_length=255, blank=True, null=True, default=None)
    fecha_nacimiento = models.IntegerField(blank=True, null=True, default=None)
    fecha_alta = models.IntegerField(blank=True, null=True, default=None)
    tipo_cuenta = models.CharField(max_length=1, blank=True, null=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Titular, self).__init__(*args, **kwargs)
        self.__important_fields = [
            'domicilio_calle', 'domicilio_barrio', 'localidad', 'provincia'
        ]
        for field in self.__important_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

        self.__change_fields = [
            'apellido', 'nombre', 'domicilio_numero', 'domicilio_piso', 'domicilio_depto'
        ]

        for field in self.__change_fields:
            setattr(self, '__original_%s' % field, getattr(self, field))

    @staticmethod
    def quitar_espacios():
        exito = True
        try:
            query = ' UPDATE contacto_titular '
            query += ' SET domicilio_barrio=UPPER(TRIM(domicilio_barrio)), '
            query += '  domicilio_calle=UPPER(TRIM(domicilio_calle)), '
            query += '  provincia=UPPER(TRIM(provincia)), '
            query += '  localidad=UPPER(TRIM(localidad)), '
            query += '  nombre=trim(nombre), '
            query += '  apellido=trim(apellido) '

            cursor = connection.cursor()
            cursor.cursor.execute(query)
        except Exception as ex:
            exito = False
            print(ex)
        finally:
            cursor.cursor.close()
        return exito

    def __str__(self):
        return u'%s - %s' % (str(self.tipo), str(self.titular))

    def __unicode__(self):
        return u'%s - %s' % (str(self.tipo), str(self.titular))

    def has_normalized(self):
        for field in self.__important_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True
        return False

    def has_changed(self):
        for field in self.__change_fields:
            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                return True
        return False

    def normalizar_contacto(self):
        contacto = ContactoNormalizado.objects.filter(titular=self.titular, tipo=self.tipo).first()
        if contacto:
            contacto.normalizado = False
            contacto.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.has_normalized():
            self.normalizar_contacto()

        super(Titular, self).save()

        # si cambiaron los datos, busco el contacto normalizado y los actualizo
        if self.has_changed():
            contacto = ContactoNormalizado.objects.filter(titular=self.titular, tipo=self.tipo).first()
            if contacto:
                contacto.apellido = self.apellido
                contacto.nombre = self.nombre
                contacto.altura = self.domicilio_numero
                contacto.piso = self.domicilio_piso
                contacto.departamento = self.domicilio_depto
                contacto.save()

