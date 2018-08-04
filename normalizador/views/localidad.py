# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models.localidad import Localidad
from normalizador.serializers.localidad import LocalidadSerializer, LocalidadCuadrantesSerializer


class LocalidadViewSet(viewsets.ModelViewSet):
    """
      retrieve:
          Retorna una localidad.

      list:
          Retorna el listado de todas las localidades.

          Filtros:

              Se pueden filtrar las localidades por nombre utilizando el parametro search.
              Ejemplo: localhost/v1/localidad/?search=texto

      create:
          Crea una nueva localidad.

      delete:
          Elimina la localidad.

      update:
          Actualiza todos los campos de la localidad.

      partial_update:
          Actualiza uno o más campos de la localidad.

      """

    queryset = Localidad.objects.filter(
        estado=ACTIVO,
        provincia__estado=ACTIVO
    ).order_by('nombre')
    serializer_class = LocalidadSerializer
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
            'localidades':serializer.data
        }
        return Response(result)

class LocalidadCuadrantesRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Localidad.objects.filter(
        estado=ACTIVO,
        provincia__estado=ACTIVO
    )
    serializer_class = LocalidadCuadrantesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


