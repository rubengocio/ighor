# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.models.filtro_calle import FiltroCalle


class FiltroCalleSerializer(serializers.ModelSerializer):

    class Meta:
        model = FiltroCalle
        fields = (
            'operador',
            'parentesis_abierto',
            'criterio',
            'valor',
            'parentesis_cerrado'
        )