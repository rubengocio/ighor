# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from contacto.models import ContactoNormalizado
from normalizador import errors
from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models import DiccionarioBarrio
from normalizador.models import DiccionarioCalle
from normalizador.models.calle import Calle
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.calle import CalleSerializer


class CalleViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Retorna una Calle.

    list:
        Retorna el listado de todas las calles

        Filtros:

                  Se pueden filtrar las calles por nombre utilizando el parametro search.
                  Ejemplo: localhost/v1/calle/?search=texto

    create:
        Crea una nueva calle.

    delete:
        Elimina una calle.

    update:
        Actualiza todos los valores de una calle.

    partial_update:
        Actualiza uno o mas valores de una calle.

    """
    queryset = Calle.objects.filter(estado=ACTIVO).order_by('nombre')
    serializer_class = CalleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def validate_delete(self, obj):
        if ContactoNormalizado.objects.filter(calle=obj).exists():
            return False

        if CallesBarrio.objects.filter(calle=obj).exists():
            return False

        if DiccionarioCalle.objects.filter(calle_barrio__calle=obj).exists():
            return False

        return True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.validate_delete(instance) is False:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={errors.ERROR_CALLE})
        else:
            instance.estado = INACTIVO
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        search = request.GET.get('search', None)
        if search:
            queryset=queryset.filter(nombre__icontains=search)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        result={
            'calles':serializer.data
        }
        return Response(result)