# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.serializers.cuadrante import CuadranteSerializer


class BarrioSerializer(serializers.ModelSerializer):
    cuadrante = CuadranteSerializer()

    class Meta:
        model = Barrio
        fields = (
            'id',
            'nombre',
            'codigo_postal',
            'cuadrante'
        )

    def validar_nombre(self, nombre, cuadrante, instance=None):
        barrios=Barrio.objects.filter(
            nombre__iexact=nombre,
            cuadrante=cuadrante,
            estado=ACTIVO
        )

        if instance:
            barrios=barrios.exclude(id=instance.id)

        if barrios.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.BARRIO_EXISTE]})

    def create(self, validated_data):
        id = self.initial_data.get('cuadrante').get('id', None)
        cuadrante = Cuadrante.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'cuadrante': [constants.CAMPO_REQUERIDO]})
        elif not cuadrante:
            raise serializers.ValidationError({'cuadrante': [constants.CUADRANTE_NO_EXISTE]})

        nombre = validated_data.get('nombre', None)
        self.validar_nombre(nombre, cuadrante)

        validated_data['cuadrante'] = cuadrante

        instance = Barrio.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        nombre = validated_data.get('nombre', None)
        id = self.initial_data.get('cuadrante').get('id', None)
        cuadrante = Cuadrante.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'cuadrante': [constants.CAMPO_REQUERIDO]})
        elif not cuadrante:
            raise serializers.ValidationError({'cuadrante': [constants.CUADRANTE_NO_EXISTE]})

        self.validar_nombre(nombre, cuadrante, instance)
        instance.save()
        return instance


class BarrioCallesSerializer(serializers.ModelSerializer):
    cuadrante = CuadranteSerializer()
    calles = serializers.SerializerMethodField()

    class Meta:
        model = Barrio
        fields = (
            'id',
            'nombre',
            'codigo_postal',
            'cuadrante',
            'calles'
        )

    def get_calles(self, obj):
        resutl = []
        return resutl
