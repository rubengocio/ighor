# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from normalizador.enum import ACTIVO, INACTIVO
from normalizador.models.provincia import Provincia
from normalizador.serializers.provincia import ProvinciaSerializer, ProvinciaLocalidadesSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user instance.

    list:
        Return all users, ordered by most recently joined.

    create:
        Create a new user.

    delete:
        Remove an existing user.

    partial_update:
        Update one or more fields on an existing user.

    """
    queryset = Provincia.objects.filter(estado=ACTIVO)
    serializer_class = ProvinciaSerializer
    permission_classes = [permissions.IsAuthenticated]


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado=INACTIVO
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