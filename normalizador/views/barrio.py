# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models.barrio import Barrio
from normalizador.serializers.barrio import BarrioSerializer, BarrioCallesSerializer


class BarrioViewSet(viewsets.ModelViewSet):
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO,
        cuadrante__localidad__estado=ACTIVO,
        cuadrante__localidad__provincia__estado=ACTIVO
    )
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado=INACTIVO
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BarrioCallesRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO,
        cuadrante__localidad__estado=ACTIVO,
        cuadrante__localidad__provincia__estado=ACTIVO
    )
    serializer_class = BarrioCallesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)