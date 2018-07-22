# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.localidad import Localidad
from normalizador.serializers.localidad import LocalidadSerializer, LocalidadCuadrantesSerializer


class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.filter(estado=ACTIVO, provincia__estado=ACTIVO)
    serializer_class = LocalidadSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocalidadCuadrantesRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Localidad.objects.filter(estado=ACTIVO, provincia__estado=ACTIVO)
    serializer_class = LocalidadCuadrantesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
