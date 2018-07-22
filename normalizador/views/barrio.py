# -*- coding: utf-8 -*-
from rest_framework import permissions
from rest_framework import viewsets


from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.serializers.barrio import BarrioSerializer


class BarrioViewSet(viewsets.ModelViewSet):
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO,
    )
    serializer_class = BarrioSerializer
    permission_classes = [permissions.IsAuthenticated]