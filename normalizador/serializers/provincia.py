# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.enum import ACTIVO
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia
from django.utils.translation import ugettext_lazy as _


class ProvinciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provincia
        fields = (
            'id',
            'nombre',
        )

    def validar_nombre(self, nombre, instance=None):
        provincias=Provincia.objects.filter(nombre__iexact=nombre, estado=ACTIVO)

        if instance:
            provincias=provincias.exclude(id=instance.id)

        if provincias.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.PROVINCIA_EXISTS]})


    def create(self, validated_data):
        nombre=validated_data.get('nombre', None)
        self.validar_nombre(nombre)
        instance = Provincia.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        nombre = validated_data.get('nombre', None)
        self.validar_nombre(nombre, instance)
        instance.save()
        return instance


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