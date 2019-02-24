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
    normalizado = models.BooleanField(default=False, db_index=True)
    fecha_actualizacion=models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together=('tipo', 'titular',)

    @staticmethod
    def actualizar_contacto():
        exito = True
        try:
            query = ' insert into contacto_contactonormalizado(tipo, titular, apellido, nombre, altura, piso, departamento, estado) '
            query += ' select tipo, titular, apellido, nombre, domicilio_numero, domicilio_piso, domicilio_depto,1 '
            query += ' from contacto_titular '
            query += ' where not exists (select 1 from contacto_contactonormalizado   '
            query += '                      where contacto_contactonormalizado.tipo=contacto_titular.tipo '
            query += '                      and contacto_contactonormalizado.titular=contacto_titular.titular) '

            cursor = connection.cursor()
            cursor.cursor.execute(query)

        except Exception as ex:
            print(ex.message)
            exito = False
        finally:
            cursor.cursor.close()
        return exito

    @staticmethod
    def actualizar_barrios():
        exito = True

        query = ' UPDATE contacto_contactonormalizado '
        query += '   SET barrio_id = (SELECT normalizador_diccionariobarrio.barrio_id '
        query += '                  FROM contacto_titular   '
        query += '                  INNER JOIN normalizador_diccionariobarrio ON contacto_titular.domicilio_barrio = normalizador_diccionariobarrio.nombre '
        query += '                  INNER JOIN normalizador_barrio ON normalizador_barrio.id = normalizador_diccionariobarrio.barrio_id AND normalizador_barrio.estado=1 '
        query += '                  INNER JOIN normalizador_cuadrante ON normalizador_cuadrante.id = normalizador_barrio.cuadrante_id '
        query += '                  WHERE contacto_titular.titular = contacto_contactonormalizado.titular and contacto_titular.tipo = contacto_contactonormalizado.tipo '
        query += '                  AND normalizador_cuadrante.localidad_id = contacto_contactonormalizado.localidad_id '
        query += '                  AND normalizador_diccionariobarrio.barrio_id is not null '
        query += '                  AND contacto_contactonormalizado.localidad_id is not null) '
        query += '  WHERE normalizado=0 '

        try:
            cursor = connection.cursor()
            cursor.cursor.execute(query)
        except Exception as ex:
            exito = False
            print(str(ex))
        finally:
            cursor.cursor.close()

        return exito

    @staticmethod
    def actualizar_barrio(diccionario_barrios, barrio):
        cant = 0
        try:
            barrios_incorrectos = diccionario_barrios.values_list('id', flat=True)

            ids=','.join(str(x) for x in barrios_incorrectos)

            query = ' SELECT contacto_titular.tipo, '
            query += ' contacto_titular.titular '
            query += ' FROM contacto_titular '
            query += ' INNER JOIN normalizador_diccionariobarrio ON normalizador_diccionariobarrio.nombre = contacto_titular.domicilio_barrio '
            query += ' WHERE normalizador_diccionariobarrio.id IN ( ' + ids + ' ) '

            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                contacto=ContactoNormalizado.objects.get(tipo=row[0], titular=row[1])
                contacto.barrio=barrio
                contacto.fecha_actualizacion=datetime.now()
                contacto.save()
                cant += 1
        except Exception as ex:
            pass
        finally:
            cursor.close()
        return cant

    @staticmethod
    def actualizar_calles():
        exito = True

        query = ' UPDATE contacto_contactonormalizado '
        query += '      SET calle_id = (SELECT MAX(normalizador_calle.id) '
        query += '                      FROM normalizador_diccionariocalle '
        query += '                      INNER JOIN normalizador_calleincorrecta ON normalizador_calleincorrecta.id = normalizador_diccionariocalle.calle_incorrecta_id '
        query += '                      INNER JOIN normalizador_callesbarrio ON normalizador_callesbarrio.id = normalizador_diccionariocalle.calle_barrio_id '
        query += '                      INNER JOIN normalizador_calle ON normalizador_calle.id = normalizador_callesbarrio.calle_id AND normalizador_calle.estado = 1 '
        query += '                      INNER JOIN contacto_titular ON contacto_titular.domicilio_calle = normalizador_calleincorrecta.nombre '
        query += '                      WHERE contacto_titular.titular = contacto_contactonormalizado.titular '
        query += '                      AND contacto_titular.tipo = contacto_contactonormalizado.tipo '
        query += '                      AND normalizador_callesbarrio.barrio_id = contacto_contactonormalizado.barrio_id '
        query += '                      AND contacto_contactonormalizado.barrio_id is not null ) '
        query += '  WHERE normalizado=0 '

        try:
            cursor = connection.cursor()
            cursor.cursor.execute(query)
        except Exception as ex:
            exito = False
            print(str(ex))
        finally:
            cursor.cursor.close()

        return exito

    @staticmethod
    def actualizar_calle(diccionario_calles, calle_barrio):
        cant = 0
        try:
            ids = ','.join(str(x.id) for x in diccionario_calles)

            query = ' SELECT contacto_titular.tipo, '
            query += ' contacto_titular.titular '
            query += ' FROM contacto_titular '
            query += ' INNER JOIN normalizador_calleincorrecta ON normalizador_calleincorrecta.nombre = contacto_titular.domicilio_calle '
            query += ' INNER JOIN normalizador_diccionariocalle ON normalizador_diccionariocalle.calle_incorrecta_id = normalizador_calleincorrecta.id AND normalizador_diccionariocalle.calle_barrio_id=%s'
            query += ' WHERE normalizador_diccionariocalle.id IN ( %s ) '

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
        finally:
            cursor.close()
        return cant

    @staticmethod
    def actualizar_provincia():
        exito = True

        query = ' UPDATE contacto_contactonormalizado '
        query += '  SET provincia_id = (SELECT MAX(normalizador_provincia.id) '
        query += '      FROM contacto_titular '
        query += '      INNER JOIN normalizador_provincia ON (normalizador_provincia.nombre=contacto_titular.provincia AND normalizador_provincia.estado=1) '
        query += '      WHERE contacto_contactonormalizado.titular=contacto_titular.titular AND contacto_contactonormalizado.tipo=contacto_titular.tipo) '
        query += '  WHERE normalizado=0 '

        try:
            cursor = connection.cursor()
            cursor.cursor.execute(query)
        except Exception as ex:
            exito = False
            print(str(ex))
        finally:
            cursor.cursor.close()

        return exito

    @staticmethod
    def actualizar_localidad():
        exito = True

        query = ' UPDATE contacto_contactonormalizado '
        query += ' SET localidad_id = (SELECT normalizador_localidad.id '
        query += '          FROM contacto_titular '
        query += '          INNER JOIN normalizador_localidad ON (normalizador_localidad.nombre=contacto_titular.localidad AND normalizador_localidad.estado=1) '
        query += '          WHERE contacto_titular.titular = contacto_contactonormalizado.titular AND contacto_titular.tipo = contacto_contactonormalizado.tipo  '
        query += '          AND contacto_contactonormalizado.provincia_id = normalizador_localidad.provincia_id) '
        query += ' WHERE contacto_contactonormalizado.provincia_id is not null '
        query += ' AND normalizado=0 '

        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as ex:
            exito = False
            print(str(ex))
        finally:
            cursor.close()
        return exito

    @staticmethod
    def actualizar_normalizados():
        exito = True

        query = ' UPDATE contacto_contactonormalizado '
        query += ' SET normalizado = (CASE WHEN provincia_id is not null and localidad_id is not null and '
        query += '                          barrio_id is not null and calle_id is not null THEN 1 else 0 END)'
        query += ' WHERE normalizado=0 '

        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as ex:
            exito = False
            print(str(ex))
        finally:
            cursor.close()
        return exito