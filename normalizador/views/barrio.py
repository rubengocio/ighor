# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from contacto.models import ContactoNormalizado
from normalizador import errors
from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models import DiccionarioBarrio
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.barrio import BarrioSerializer


class BarrioViewSet(viewsets.ModelViewSet):
    """
          retrieve:
              Retorna un barrio.

          list:
              Retorna el listado de todos los barrios.

              Filtros:

                  Se pueden filtrar los barrios por nombre utilizando el parametro search.
                  Ejemplo: localhost/v1/barrio/?search=texto

          create:
              Crea un nuevo barrio.

          delete:
              Elimina un barrio.

          update:
              Actualiza todos los campos de un barrio.

          partial_update:
              Actualiza uno o más campos de un barrio.

    """

    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO,
        cuadrante__localidad__estado=ACTIVO,
        cuadrante__localidad__provincia__estado=ACTIVO
    ).order_by('nombre')
    serializer_class = BarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            'barrios':serializer.data
        }
        return Response(result)

    def validate_delete(self, obj):
        if ContactoNormalizado.objects.filter(barrio=obj).exists():
            return False

        if CallesBarrio.objects.filter(barrio=obj).exists():
            return False

        if DiccionarioBarrio.objects.filter(barrio=obj).exists():
            return False

        return True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.validate_delete(instance) is False:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={errors.ERROR_BARRIO})
        else:
            instance.estado = INACTIVO
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)