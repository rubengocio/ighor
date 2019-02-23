# -*- coding: utf-8 -*-
from django.db import models, connection


class CalleIncorrecta(models.Model):
    nombre = models.CharField(max_length=127, db_index=True)

    def __str__(self):
        return u'%s' % self.nombre

    def __unicode__(self):
        return u'%s' % self.nombre

    @staticmethod
    def actualizar_calle_incorrecta(barrio_id):
        try:
            query = ' INSERT INTO normalizador_calleincorrecta(nombre) '
            query += ' SELECT contacto_titular.domicilio_calle '
            query += ' FROM contacto_titular '
            query += ' INNER JOIN normalizador_diccionariobarrio ON (normalizador_diccionariobarrio.barrio_id=%s AND normalizador_diccionariobarrio.nombre=contacto_titular.domicilio_barrio) '
            query += ' WHERE NOT EXISTS (SELECT 1 FROM normalizador_calleincorrecta WHERE normalizador_calleincorrecta.nombre=contacto_titular.domicilio_calle) '
            query += ' GROUP BY contacto_titular.domicilio_calle '
            query = query % str(barrio_id)
            cursor = connection.cursor()
            cursor.execute(query)

        except Exception as ex:
            print(ex)
            return False
        return True


