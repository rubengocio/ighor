# -*- coding: utf-8 -*-
from django.db import models, connection

from normalizador.enum import ESTADO_CHOICES, ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia
from datetime import datetime


class ContactoNormalizado(models.Model):
    tipo = models.IntegerField(blank=True, null=True, default=0)
    titular = models.IntegerField(blank=True, null=True, default=0)
    apellido = models.CharField(max_length=255, blank=True, null=True, default=None)
    nombre = models.CharField(max_length=255, blank=True, null=True, default=None)
    provincia = models.ForeignKey(Provincia, blank=True, null=True)
    localidad = models.ForeignKey(Localidad, blank=True, null=True)
    barrio = models.ForeignKey(Barrio, blank=True, null=True)
    calle = models.ForeignKey(Calle ,blank=True, null=True)
    altura = models.CharField(max_length=255, blank=True, null=True, default=None)
    piso=models.CharField(max_length=255, blank=True, null=True, default=None)
    departamento=models.CharField(max_length=255, blank=True, null=True, default=None)
    observaciones=models.CharField(max_length=255, blank=True, null=True, default=None)
    estado = models.IntegerField(choices=ESTADO_CHOICES, db_index=True, default=ACTIVO)
    fecha_actualizacion=models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together=('tipo', 'titular',)

    @staticmethod
    def actualizar_contacto():
        try:
            query = ' insert into contacto_contactonormalizado(tipo, titular, apellido, nombre, altura, piso, departamento, estado) '
            query += ' select tipo, titular, apellido, nombre, domicilio_numero, domicilio_piso, domicilio_depto,1 '
            query += ' from contacto_titular '
            query += ' where not exists (select 1 from contacto_contactonormalizado where contacto_contactonormalizado.tipo=contacto_titular.tipo and contacto_contactonormalizado.titular=contacto_titular.titular) '

            cursor = connection.cursor()
            cursor.execute(query)

        except Exception as ex:
            print(ex.message)
            return False
        return True

    @staticmethod
    def actualizar_barrio(diccionario_barrios, barrio):
        cant = 0
        try:
            barrios_incorrectos=diccionario_barrios.values_list('id', flat=True)

            ids=','.join(str(x) for x in barrios_incorrectos)

            query = ' SELECT "contacto_titular"."tipo", '
            query += ' "contacto_titular"."titular" '
            query += ' FROM "contacto_titular" '
            query += ' INNER JOIN "normalizador_diccionariobarrio" ON "normalizador_diccionariobarrio"."nombre" = "contacto_titular"."domicilio_barrio" '
            query += ' WHERE "normalizador_diccionariobarrio"."id" IN ( ' + ids + ' ) '

            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                contacto=ContactoNormalizado.objects.get(tipo=row[0], titular=row[1])
                contacto.barrio=barrio
                contacto.fecha_actualizacion=datetime.now()
                contacto.save()
                cant += 1
        except Exception:
            pass
        return cant

    @staticmethod
    def actualizar_calle(diccionario_calles, calle_barrio):
        cant = 0
        try:
            ids = ','.join(str(x.id) for x in diccionario_calles)

            query = ' SELECT "contacto_titular"."tipo", '
            query += ' "contacto_titular"."titular" '
            query += ' FROM "contacto_titular" '
            query += ' INNER JOIN "normalizador_calleincorrecta" ON "normalizador_calleincorrecta"."nombre" = "contacto_titular"."domicilio_calle" '
            query += ' INNER JOIN "normalizador_diccionariocalle" ON "normalizador_diccionariocalle"."calle_incorrecta_id" = "normalizador_calleincorrecta"."id" AND "normalizador_diccionariocalle"."calle_barrio_id"=%s'
            query += ' WHERE "normalizador_diccionariocalle"."id" IN ( %s ) '

            query = query % (calle_barrio.id, ids)

            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                contacto = ContactoNormalizado.objects.get(tipo=row[0], titular=row[1])
                contacto.barrio = calle_barrio.barrio
                contacto.calle = calle_barrio.calle
                contacto.fecha_actualizacion = datetime.now()
                contacto.save()
                cant += 1
        except Exception:
            pass
        return cant

    @staticmethod
    def actualizar_provincia():
        try:
            query = ' UPDATE "contacto_contactonormalizado" '
            query += ' SET "provincia_id" = %s '
            query += ' WHERE "contacto_contactonormalizado"."id" IN ( '
            query += ' SELECT "contacto_contactonormalizado"."id" '
            query += ' FROM "contacto_titular" '
            query += ' INNER JOIN "normalizador_provincia" ON ("normalizador_provincia"."nombre"="contacto_titular"."provincia" AND "normalizador_provincia"."id"=%s)  '
            query += ' INNER JOIN "contacto_contactonormalizado" ON ("contacto_contactonormalizado"."tipo"="contacto_titular"."tipo" AND "contacto_contactonormalizado"."titular"="contacto_titular"."titular") ) '

            provincias = Provincia.objects.all()
            for provincia in provincias:
                query_1 = query % (provincia.id, provincia.id)

                cursor = connection.cursor()
                cursor.execute(query_1)
        except Exception:
            pass
        return True

    @staticmethod
    def actualizar_localidad():
        try:
            query = ' UPDATE "contacto_contactonormalizado" '
            query += ' SET "localidad_id" = %s '
            query += ' WHERE "contacto_contactonormalizado"."id" IN ( '
            query += ' SELECT "contacto_contactonormalizado"."id" '
            query += ' FROM "contacto_titular" '
            query += ' INNER JOIN "normalizador_localidad" ON ("normalizador_localidad"."nombre"="contacto_titular"."localidad" AND "normalizador_localidad"."id"=%s)  '
            query += ' INNER JOIN "contacto_contactonormalizado" ON ("contacto_contactonormalizado"."tipo"="contacto_titular"."tipo" AND "contacto_contactonormalizado"."titular"="contacto_titular"."titular") ) '

            localidades = Localidad.objects.all()
            for localidad in localidades:
                query_1 = query % (localidad.id, localidad.id)

                cursor = connection.cursor()
                cursor.execute(query_1)
        except Exception:
            pass
        return True