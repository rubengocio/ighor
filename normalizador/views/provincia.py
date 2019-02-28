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
from normalizador.models.provincia import Provincia
from normalizador.serializers.provincia import ProvinciaSerializer, ProvinciaLocalidadesSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Retorna una provincia.

    list:
        Retorna el listado de provincias.

        Filtros:

            Se pueden filtrar las provincias por nombre utilizando el parametro search.
            Ejemplo: localhost/v1/provincia/?search=texto

    create:
        Crea una nueva provincia.

    delete:
        Elimina la provincia.

    update:
        Actualiza todos los campos de la provincia.

    partial_update:
        Actualiza uno o más campos de la provincia.

    """
    queryset = Provincia.objects.filter(estado=ACTIVO).order_by('nombre')
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def validate_delete(self, obj):

        if ContactoNormalizado.objects.filter(provincia=obj).exists():
            return False

        if DiccionarioBarrio.objects.filter(barrio__cuadrante__localidad__provincia=obj).exists():
            return False

        return True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.validate_delete(instance) is False:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={errors.ERROR_PROVINCIA})
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
            'provincias':serializer.data
        }
        return Response(result)


class ProvinciaLocalidadesRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de localidades de una provincia
    """

    queryset = Provincia.objects.filter(estado=ACTIVO)
    serializer_class = ProvinciaLocalidadesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request,*args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)