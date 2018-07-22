# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.cuadrante import Cuadrante
from normalizador.serializers.cuadrante import CuadranteSerializer, CuadranteBarriosSerializer


class CuadranteViewSet(viewsets.ModelViewSet):
    queryset = Cuadrante.objects.filter(estado=ACTIVO)
    serializer_class = CuadranteSerializer
    permission_classes = [permissions.IsAuthenticated]


class CuadranteBarriosRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Cuadrante.objects.filter(estado=ACTIVO)
    serializer_class = CuadranteBarriosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)