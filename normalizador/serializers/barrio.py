# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.models.barrio import Barrio


class BarrioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Barrio
        fields = (
            'id',
            'nombre',
            'codigo_postal',
            'cuadrante'
        )
