# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.serializers.localidad import LocalidadSerializer


class CuadranteSerializer(serializers.ModelSerializer):
    localidad=LocalidadSerializer()

    class Meta:
        model = Cuadrante
        fields = (
            'id',
            'nombre',
            'localidad'
        )

    def validar_nombre(self, nombre, localidad, instance=None):
        cuadrantes = Cuadrante.objects.filter(
            nombre__iexact=nombre,
            localidad=localidad,
            estado=ACTIVO
        )

        if instance:
            cuadrantes = cuadrantes.exclude(id=instance.id)

        if cuadrantes.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.CUADRANTE_EXISTE]})

    def create(self, validated_data):
        id = self.initial_data.get('localidad').get('id', None)
        localidad = Localidad.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'localidad': [constants.CAMPO_REQUERIDO]})
        elif not localidad:
            raise serializers.ValidationError({'localidad': [constants.LOCALIDAD_NO_EXISTE]})

        validated_data['localidad']=localidad

        nombre = validated_data.get('nombre', None)
        self.validar_nombre(nombre, localidad)

        instance=Cuadrante.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        nombre = validated_data.get('nombre', None)
        id = self.initial_data.get('localidad').get('id', None)
        localidad = Localidad.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'localidad': [constants.CAMPO_REQUERIDO]})
        elif not localidad:
            raise serializers.ValidationError({'localidad': [constants.LOCALIDAD_NO_EXISTE]})

        self.validar_nombre(nombre, localidad, instance)

        if nombre:
            instance.nombre = nombre

        if localidad:
            instance.localidad = localidad

        instance.save()
        return instance



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

