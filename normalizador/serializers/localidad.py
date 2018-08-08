# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.enum import ACTIVO
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia
from normalizador.serializers.provincia import ProvinciaSerializer
from django.utils.translation import ugettext_lazy as _


class LocalidadSerializer(serializers.ModelSerializer):
    provincia = ProvinciaSerializer()

    class Meta:
        model = Localidad
        fields = (
            'id',
            'nombre',
            'provincia',
        )

    def validar_nombre(self, nombre, provincia, instance=None):
        localidades=Localidad.objects.filter(
            nombre__iexact=nombre,
            provincia=provincia,
            estado=ACTIVO
        )

        if instance:
            localidades=localidades.exclude(id=instance.id)

        if localidades.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.LOCALIDA_EXISTE]})

    def create(self, validated_data):
        id=self.initial_data.get('provincia').get('id', None)
        provincia=Provincia.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'provincia': [constants.CAMPO_REQUERIDO]})
        elif not provincia:
            raise serializers.ValidationError({'provincia':[constants.PROVINCIA_NO_EXISTE]})

        nombre = validated_data.get('nombre', None)
        self.validar_nombre(nombre, provincia)

        validated_data['provincia']=provincia
        instance = Localidad.objects.create(**validated_data)

        return instance


    def update(self, instance, validated_data):
        nombre = validated_data.get('nombre', None)
        codigo_postal = validated_data.get('codigo_postal', None)
        id = self.initial_data.get('provincia').get('id', None)
        provincia = Provincia.objects.filter(pk=id).first()
        if not id:
            raise serializers.ValidationError({'provincia': [constants.CAMPO_REQUERIDO]})
        elif not provincia:
            raise serializers.ValidationError({'provincia':[constants.PROVINCIA_NO_EXISTE]})

        self.validar_nombre(nombre, provincia, instance)

        if nombre:
            instance.nombre = nombre

        if codigo_postal:
            instance.codigo_postal = codigo_postal

        if provincia:
            instance.provincia=provincia

        instance.save()
        return instance


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

