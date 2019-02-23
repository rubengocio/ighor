# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio


class ReporteNormalizacionBarrioAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        "cantidad_registros_diccionario": cantidad total de registros en el diccionario de barrios,
        "cantidad_registros_normalizados_diccionario": cantidad de registros normalizados en el diccionario de barrios,
        "cantidad_registros_normalizados_por_sector_diccionario": cantidad de registros normalizados del sector en el diccionario de barrios,
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

        query = "  select count(*) as total_registros, "
        query += " 	    count(case when normalizador_diccionariobarrio.barrio_id is null then null else normalizador_diccionariobarrio.barrio_id end) as cant_barrio_normalizado, "
        query += " 	    count(case when normalizador_barrio.cuadrante_id = " + cuadrante_id + " then normalizador_diccionariobarrio.barrio_id else null end) as cant_barrios_por_sector "
        query += " from normalizador_diccionariobarrio  "
        query += " left join normalizador_barrio on normalizador_barrio.id = normalizador_diccionariobarrio.barrio_id "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_diccionario': rows[0][0],
            'cantidad_registros_normalizados_diccionario': rows[0][1],
            'cantidad_registros_normalizados_por_sector_diccionario': rows[0][2],
        }

        return Response(result, status=status.HTTP_200_OK)


class ReporteNormalizacionCallesBarrioAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        "cantidad_calles_por_barrio": cantidad de calles por barrio
	    "cantidad_registros_total": cantidad total de registros
	    "cantidad_registros_calle_normalizado_por_barrio": cantidad de usuarios normalizados por barrio
	    "cantidad_registros_calle_normalizado": cantidad de usuarios normalizados por calle

    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CallesBarrio.objects.filter(
        barrio__estado=ACTIVO,
        barrio__cuadrante__estado=ACTIVO
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        calle_id = str(instance.calle.id)
        barrio_id = str(instance.barrio.id)

        query = " select count(*) as total_registros, "
        query += " 	    sum(case when calle_id=" + calle_id + " and barrio_id=" + barrio_id + " then 1 else 0 end) as cant_registros_calle_normalizado, "
        query += " 	    (select count(*) from normalizador_callesbarrio where normalizador_callesbarrio.barrio_id=" + barrio_id + ") as cant_calles_por_barrio, "
        query += " 	    (select count(contacto_contactonormalizado.calle_id)  "
        query += " 	     from normalizador_callesbarrio  "
        query += " 	     inner join normalizador_calle on  normalizador_calle.id=normalizador_callesbarrio.calle_id "
        query += " 	     inner join contacto_contactonormalizado on contacto_contactonormalizado.barrio_id=normalizador_callesbarrio.barrio_id and contacto_contactonormalizado.calle_id=normalizador_callesbarrio.calle_id  "
        query += " 	     where normalizador_callesbarrio.barrio_id=" + barrio_id + ") as cant_registros_calle_normalizado_por_barrio  "
        query += " from contacto_contactonormalizado  "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_total': rows[0][0],
            'cantidad_registros_calle_normalizado': rows[0][1],
            'cantidad_calles_por_barrio': rows[0][2],
            'cantidad_registros_calle_normalizado_por_barrio': rows[0][3],
        }

        return Response(result, status=status.HTTP_200_OK)



