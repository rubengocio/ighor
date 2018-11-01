# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.cuadrante import Cuadrante


class ReporteNormalizacionAPIView(generics.ListAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        'cantidad_registros_barrio_normalizado': Cantidad de registros con barrio normalizado
        'cantidad_registros_barrio_calle_normalizado': Cantidad de registros con calle normalizada
        'cantidad_registros_total': cantidad total de registros (cantidad de registros base de tn)

    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):

        query = " select (select  count(*) from contacto_contactonormalizado where barrio_id is not null) as cant_barrio_normalizado, "
        query += " (select count(*) from contacto_contactonormalizado where barrio_id is not null and calle_id is not null) as cant_barrio_calle_normalizado, "
        query += " (select count(*) as cantidad from contacto_titular) as total_registros "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_barrio_normalizado': rows[0][0],
            'cantidad_registros_barrio_calle_normalizado': rows[0][1],
            'cantidad_registros_total': rows[0][2],

        }

        return Response(result, status=status.HTTP_200_OK)


class ReporteBarriosSectorRetrieveAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con la cantidad de barrios por sector

        'cantidad_barrios_sector': Cantidad de barrios del sector
        'cantidad_barrios_normalizados': Cantidad de barrios normalizados del sector
        'cantidad_registros_normalizados': cantidad de registros normalizados en el sector

    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cuadrante.objects.filter(estado=ACTIVO)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        query = "  SELECT COUNT(*) as cant_barrios_sector, "
        query += " 		SUM(CASE WHEN x.cant_barrios > 0 THEN 1 ELSE 0 END) as cant_barrios_normalizados, "
        query += " 		SUM(x.cant_registros) as cant_registros_normalizados "
        query += " FROM ( "
        query += "      SELECT normalizador_barrio.id, "
        query += "              COUNT(DISTINCT normalizador_diccionariobarrio.id) as cant_barrios, "
        query += "              COUNT(DISTINCT contacto_contactonormalizado.id) as cant_registros "
        query += "      FROM normalizador_barrio "
        query += "      LEFT JOIN contacto_contactonormalizado  on contacto_contactonormalizado.barrio_id=normalizador_barrio.id "
        query += "      LEFT JOIN normalizador_diccionariobarrio ON normalizador_diccionariobarrio.barrio_id=normalizador_barrio.id "
        query += "      WHERE normalizador_barrio.cuadrante_id= " + str(instance.id) + " "
        query += "      AND normalizador_barrio.estado=1 "
        query += "      GROUP BY normalizador_barrio.id "
        query += "  ) as x "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_barrios_sector': rows[0][0],
            'cantidad_barrios_normalizados': rows[0][1],
            'cantidad_registros_normalizados': rows[0][2],
        }

        return Response(result, status=status.HTTP_200_OK)


