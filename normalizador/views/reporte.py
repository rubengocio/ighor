# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


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