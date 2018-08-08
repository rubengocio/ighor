# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.models.calles_barrio import CallesBarrio


class CallesBarrioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallesBarrio
        fields = (
            'id',
            'barrio',
            'calle',
            'altura_desde',
            'altura_hasta',
            'referencia',
            'plano',
            'ubicacion',
            'nomenclado'
        )
