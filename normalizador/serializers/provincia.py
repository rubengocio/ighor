# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.enum import ACTIVO
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provincia
        fields = (
            'id',
            'nombre',
        )

class ProvinciaLocalidadesSerializer(serializers.ModelSerializer):
    localidades = serializers.SerializerMethodField()

    class Meta:
        model = Provincia
        fields = (
            'id',
            'nombre',
            'localidades'
        )

    def get_localidades(self, obj):
        localidades = Localidad.objects.filter(
            provincia=obj,
            estado=ACTIVO
        ).order_by('nombre')

        result = []
        for localidad in localidades:
            result.append({
                'id': localidad.id,
                'nombre': localidad.nombre,
                'codigo_postal': localidad.codigo_postal
            })
        return result