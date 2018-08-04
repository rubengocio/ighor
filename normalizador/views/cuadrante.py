# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models.cuadrante import Cuadrante
from normalizador.serializers.cuadrante import CuadranteSerializer, CuadranteBarriosSerializer


class CuadranteViewSet(viewsets.ModelViewSet):
    """
          retrieve:
              Retorna un cuadrante.

          list:
              Retorna el listado de todos los cuadrantes.

              Filtros:

                  Se pueden filtrar los cuadrantes por nombre utilizando el parametro search.
                  Ejemplo: localhost/v1/cuadrante/?search=texto

          create:
              Crea un nuevo cuadrante.

          delete:
              Elimina un cuadrante.

          update:
              Actualiza todos los campos de un cuadrante.

          partial_update:
              Actualiza uno o más campos de un cuadrante.

    """

    queryset = Cuadrante.objects.filter(
        estado=ACTIVO,
        localidad__estado=ACTIVO,
        localidad__provincia__estado=ACTIVO
    ).order_by('nombre')
    serializer_class = CuadranteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = INACTIVO
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        search = request.GET.get('search', None)
        if search:
            queryset = queryset.filter(nombre__icontains=search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        result={
            'cuadrantes':serializer.data
        }
        return Response(result)


class CuadranteBarriosRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Cuadrante.objects.filter(
        estado=ACTIVO,
        localidad__estado=ACTIVO,
        localidad__provincia__estado=ACTIVO
    )
    serializer_class = CuadranteBarriosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)