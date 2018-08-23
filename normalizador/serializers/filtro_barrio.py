# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.models.filtro_barrio import FiltroBarrio


class FiltroBarrioSerializer(serializers.ModelSerializer):

    class Meta:
        model = FiltroBarrio
        fields = (
            'operador',
            'parentesis_abierto',
            'criterio',
            'valor',
            'parentesis_cerrado'
        )