# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from hoja_ruta.serializers import HojaRutaSerializer, GeneradorHojaRutaSerializer
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio


class GenerarHojaRutaUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )
    serializer_class = GeneradorHojaRutaSerializer


class HojaRutaCallesRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            query = ' select normalizador_calle.id,normalizador_calle.nombre,count(*) as cantidad_registros '
            query += ' from contacto_contactonormalizado '
            query += ' inner join normalizador_calle on normalizador_calle.id=contacto_contactonormalizado.calle_id '
            query += ' where contacto_contactonormalizado.barrio_id=%d '
            query += ' group by normalizador_calle.id,normalizador_calle.nombre '
            query += ' order by normalizador_calle.nombre '

            query = query % instance.id
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            result=[]
            for row in rows:
                result.append({
                    'id': row[0],
                    'nombre': row[1],
                    'cantidad_registros': row[2]
                })
        except Exception as ex:
            print(ex.message)

        return Response(result)



class HojaRutaRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()


        return Response({'data':'ok'})


"""
select contacto_titular.nombre,
		contacto_titular.apellido,
		normalizador_calle.nombre,
		contacto_contactonormalizado.altura,
		contacto_contactonormalizado.piso,
		contacto_contactonormalizado.departamento,
		normalizador_barrio.nombre,
		contacto_titular.telefono,
		contacto_cliente.productos,
		contacto_cliente.cualidad,
		contacto_cliente.meses_deuda,
		contacto_cliente.monto_deuda,
		contacto_cliente.inhumados,
		contacto_titular.titular,
		contacto_titular.estado,
		contacto_titular.tipo,
		contacto_titular.tipo_cuenta,
		contacto_contactonormalizado.observaciones
from contacto_contactonormalizado
inner join contacto_titular on (contacto_titular.tipo=contacto_contactonormalizado.tipo and contacto_titular.titular=contacto_contactonormalizado.titular)
inner join normalizador_provincia on (normalizador_provincia.id=contacto_contactonormalizado.provincia_id)
inner join normalizador_barrio on (normalizador_barrio.id=contacto_contactonormalizado.barrio_id)
inner join normalizador_calle on (normalizador_calle.id=contacto_contactonormalizado.calle_id)
left join contacto_cliente on (contacto_cliente.numero_documento=contacto_contactonormalizado.titular);
"""