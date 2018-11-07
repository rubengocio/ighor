# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from hoja_ruta.models import HistorialHojaRuta, HojaRuta, DetalleHojaRuta
from hoja_ruta.serializers import HojaRutaSerializer, GeneradorHojaRutaSerializer, HistorialHojaRutaSerializer, \
    DetalleHojaRutaSerializer
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio


class GenerarHojaRutaUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )
    serializer_class = GeneradorHojaRutaSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class BarrioHojaRutaRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )
    serializer_class = HistorialHojaRutaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        historial=HistorialHojaRuta.objects.filter(barrio=instance).order_by('-id').first()

        data=None
        if historial is None:
            data={}
        else:
            serializer = HistorialHojaRutaSerializer(historial)
            data=serializer.data

        return Response(data)


class HojaRutaRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = HojaRuta.objects.all()
    serializer_class = HojaRutaSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        data=HojaRutaSerializer(instance).data
        detalles=DetalleHojaRuta.objects.filter(hoja_ruta=instance).order_by('numero_orden')
        data['detalle_hoja_ruta']=DetalleHojaRutaSerializer(detalles, many=True).data

        return Response(data)


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
