# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from hoja_ruta.models import HistorialHojaRuta, HojaRuta, DetalleHojaRuta
from hoja_ruta.serializers import HojaRutaSerializer, GeneradorHojaRutaSerializer, HistorialHojaRutaSerializer, \
    DetalleHojaRutaSerializer, ActualizarHojaRutaSerializer
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from django.views.generic import View
from django.utils import timezone
from .render import Render


class GenerarHojaRutaUpdateAPIView(generics.UpdateAPIView):
    """
    Genera las hojas de ruta correspondientes a todas las calles del barrio ingresado y retorna el listado de las mismas
    """
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
    """
    Retorna el listado de las ultimas hojas de ruta generadas
    """
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


class HojaRutaRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = HojaRuta.objects.all()
    serializer_class = HojaRutaSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retorna el detalle de contactos asignados a la hoja de ruta
        :param request:
        :param args:
        :param kwargs:
        :return:
        Retorna el detalle de contactos asignados a la hoja de ruta
        """

        instance = self.get_object()

        data=HojaRutaSerializer(instance).data
        detalles=DetalleHojaRuta.objects.filter(hoja_ruta=instance).order_by('numero_orden')
        data['detalle_hoja_ruta']=DetalleHojaRutaSerializer(detalles, many=True).data

        return Response(data)

    def update(self, request, *args, **kwargs):
        """
        Utilizado para actualizar el vendedor a quien se asigno la hoja de ruta
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


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


class Pdf(generics.ListAPIView):
    permission_classes = (AllowAny,)
    """
    Listado de hojas de ruta en pdf

        recibe por query:
            barrio:  id de barrio del cual se desean las hojas de ruta
            hojas: si es all, devuelve todas las hojas de ruta del barrio seleccionado.
                    si es un listado de ids concatenados por coma, devuelve el listado de hojas de ruta seleccionadas.

            ejemplo: localhost:8000/v1/pdf/?barrio=20&hojas=147,148

    """
    def list(self, request, *args, **kwargs):

        id=request.GET.get('barrio', None)
        barrio=get_object_or_404(Barrio, pk=id)
        hojas=request.GET.get('hojas', 'all')
        historial=HistorialHojaRuta.objects.filter(barrio=barrio).order_by('-id').first()
        hojas_ruta = HojaRuta.objects.filter(historial=historial)

        if hojas!='all':
            hojas_ruta=hojas_ruta.filter(numero__in=list(hojas.split(',')))

        today = timezone.now()
        params = {
            'today': today,
            'hojas_ruta': hojas_ruta,
            'request': request
        }
        return Render.render('pdf.html', params)

class ActualizarHojaRutaCreateAPIView(generics.CreateAPIView):
    """
    Recibe un arreglo de hojas de ruta y actualiza cada una de ellas.
    Retorna el listado actualizado

        example:

            [
              {
                "id": 3,
                "numero": "3",
                "calle": {
                  "id": 4455,
                  "nombre": " 24 DE FEBRERO"
                },
                "altura_desde": "158",
                "altura_hasta": "158",
                "cant_registros": 1,
                "asignada_a": {
                  "id": 2,
                  "first_name": "Marina",
                  "last_name": "Gadea",
                  "email": "vendedor@vendedor.com",
                  "rol": {
                    "name": "Vendedor",
                    "id": "UVE"
                  }
                },
                "estado": {
                  "id": 1,
                  "nombre": "Sin Asignar"
                }
              },
              {
                "id": 4,
                "numero": "4",
                "calle": {
                  "id": 166,
                  "nombre": " 25 DE MAYO"
                },
                "altura_desde": "3634",
                "altura_hasta": "3634",
                "cant_registros": 1,
                "asignada_a": {
                  "id": 3,
                  "first_name": "Ruben",
                  "last_name": "Gocio",
                  "email": "vendedor2@vendedor.com",
                  "rol": {
                    "name": "Vendedor",
                    "id": "UVE"
                  }
                },
                "estado": {
                  "id": 1,
                  "nombre": "Sin Asignar"
                }
              }
            ]
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = HojaRuta.objects.all()
    serializer_class = ActualizarHojaRutaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        list=[]
        for hoja_ruta in serializer.initial_data:
            hoja=get_object_or_404(HojaRuta, id=hoja_ruta['id'])
            list.append(hoja)
            s=ActualizarHojaRutaSerializer(hoja, hoja_ruta)
            if s.is_valid():
                s.save()

        serializer=ActualizarHojaRutaSerializer(list, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
