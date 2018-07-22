# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.enum import ACTIVO
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.serializers.provincia import ProvinciaSerializer


class LocalidadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Localidad
        fields = (
            'id',
            'nombre',
            'provincia',
        )


class LocalidadCuadrantesSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer()
    cuadrantes = serializers.SerializerMethodField()

    class Meta:
        model = Localidad
        fields = (
            'id',
            'nombre',
            'provincia',
            'cuadrantes',
        )

    def get_cuadrantes(self, obj):
        cuadrantes = Cuadrante.objects.filter(
            localidad=obj,
            estado=ACTIVO
        ).order_by('nombre')

        resutl = []
        for cuadrante in cuadrantes:
            resutl.append({
                'id': cuadrante.id,
                'nombre': cuadrante.nombre
            })
        return resutl

