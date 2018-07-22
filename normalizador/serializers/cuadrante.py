# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.serializers.localidad import LocalidadSerializer


class CuadranteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cuadrante
        fields = (
            'id',
            'nombre',
            'localidad'
        )


class CuadranteBarriosSerializer(serializers.ModelSerializer):
    localidad = LocalidadSerializer()
    barrios = serializers.SerializerMethodField()

    class Meta:
        model = Cuadrante
        fields = (
            'id',
            'nombre',
            'localidad',
            'barrios'
        )

    def get_barrios(self, obj):
        barrios = Barrio.objects.filter(
            cuadrante=obj,
            estado=ACTIVO
        ).order_by('nombre')

        resutl = []
        for barrio in barrios:
            resutl.append({
                'id': barrio.id,
                'nombre': barrio.nombre
            })
        return resutl

