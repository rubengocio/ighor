# -*- coding: utf-8 -*-
from django.db import models, connection

from normalizador.models.barrio import Barrio


class DiccionarioBarrio(models.Model):
    nombre = models.CharField(max_length=127, db_index=True)
    barrio = models.ForeignKey(Barrio, blank=True, null=True)

    @staticmethod
    def actualizar_diccionario_barrio():
        exito = True
        try:
            query = ' insert into normalizador_diccionariobarrio(nombre) '
            query += ' select domicilio_barrio '
            query += ' from contacto_titular '
            query += ' where domicilio_barrio not in (select nombre from normalizador_diccionariobarrio) '
            query += ' and domicilio_barrio is not null '
            query += ' group by domicilio_barrio '

            cursor = connection.cursor()
            cursor.cursor.execute(query)

        except Exception as ex:
            exito = False
            print(ex)
        finally:
            cursor.cursor.close()
        return exito
