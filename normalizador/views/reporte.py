# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.cuadrante import Cuadrante


class ReporteNormalizacionBarrioAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        'cantidad_registros_barrio_normalizado': Cantidad de registros con barrio normalizado
        'cantidad_registros_barrio_calle_normalizado': Cantidad de registros con calle normalizada
        'cantidad_registros_total': cantidad total de registros (cantidad de registros base de tn)

        "cantidad_registros_barrio_normalizado_por_sector": cantidad de ,
        "cantidad_registros_barrio_normalizado": cantidad de usuarios normalizados del barrio,
        "cantidad_barrios_por_sector": cantidad de barrios por sector,
        "cantidad_registros_total": cantidad total de registros

    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        barrio_id=str(instance.id)
        cuadrante_id=str(instance.cuadrante.id)

        query = " select count(*) as total_registros, "
        query += " 	    count(case when barrio_id=20 then 1 else 0 end) as cant_barrio_normalizado, "
        query += " 	    (select count(*) from normalizador_barrio where normalizador_barrio.cuadrante_id="+ barrio_id + " AND normalizador_barrio.estado=1) as cant_barrios_por_sector, "
        query += " 	    (select count(contacto_contactonormalizado.barrio_id)  "
        query += " 	     from normalizador_barrio  "
        query += " 	     inner join contacto_contactonormalizado on contacto_contactonormalizado.barrio_id=normalizador_barrio.id "
        query += " 	     where normalizador_barrio.cuadrante_id=" + cuadrante_id + "  "
        query += " 	     AND normalizador_barrio.estado=1) as cant_barrio_normalizado_por_sector  "
        query += " from contacto_contactonormalizado  "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_total': rows[0][0],
            'cantidad_registros_barrio_normalizado': rows[0][1],
            'cantidad_barrios_por_sector': rows[0][2],
            'cantidad_registros_barrio_normalizado_por_sector': rows[0][3],
        }

        return Response(result, status=status.HTTP_200_OK)



