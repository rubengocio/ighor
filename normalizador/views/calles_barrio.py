# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.barrio import BarrioSerializer
from normalizador.serializers.calles_barrio import CallesBarrioSerializer, CallesBarrioSimpleSerializer


class CallesBarrioViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Retorna un objeto con una relacion calle por barrio.

        tipo_numeracion:
            Par: 1
            Impar: 2
            Todas las numeraciones: 3

    list:
        Retorna el listado de relaciones calles por barrio

        tipo_numeracion:
            Par: 1
            Impar: 2
            Todas las numeraciones: 3

        Filtros:

                  Se pueden filtrar las calles y los barrios por nombre utilizando el parametro search.
                  Ejemplo: http://localhost:8000/v1/barrio_calle/?search=ANACREONTE

    create:
        Crea un objeto con una relacion calle por barrio.

        tipo_numeracion:
            Par: 1
            Impar: 2
            Todas las numeraciones: 3

    delete:
        Elimina una calle por barrio.

    update:
        Actualiza todos los valores de una calle por barrio.

        tipo_numeracion:
            Par: 1
            Impar: 2
            Todas las numeraciones: 3

    partial_update:
        Actualiza uno o mas valores de una calle por barrio.

        tipo_numeracion:
            Par: 1
            Impar: 2
            Todas las numeraciones: 3

    """
    queryset = CallesBarrio.objects.all().order_by('calle')
    serializer_class = CallesBarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        search = request.GET.get('search', None)
        if search:
            queryset=queryset.filter(Q(calle__nombre__icontains=search)|Q(barrio__nombre__icontains=search))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        result={
            'calles_barrio':serializer.data
        }
        return Response(result)


class BarrioCallesListAPIView(generics.ListAPIView):
    """
      list:
          Retorna el listado de calles asociadas al barrio ingresado.

    """

    queryset = CallesBarrio.objects.all().order_by('calle')
    serializer_class = CallesBarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        barrio = get_object_or_404(Barrio, pk=pk)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(barrio__id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


        calles = CallesBarrioSimpleSerializer(queryset, many=True).data

        result={
            'barrio': BarrioSerializer(barrio).data,
            'calles': calles
        }
        return Response(result)