# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.provincia import Provincia
from normalizador.serializers.provincia import ProvinciaSerializer, ProvinciaLocalidadesSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.filter(estado=ACTIVO)
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.IsAuthenticated]


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