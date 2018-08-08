# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.enum import ACTIVO
from normalizador.models.calle import Calle


class CalleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calle
        fields = (
            'id',
            'nombre',
        )

    def validar_nombre(self, nombre, instance=None):
        calles=Calle.objects.filter(nombre__iexact=nombre, estado=ACTIVO)

        if instance:
            calles=calles.exclude(id=instance.id)

        if calles.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.CALLE_EXISTS]})


    def create(self, validated_data):
        nombre=validated_data.get('nombre', None)
        self.validar_nombre(nombre)
        instance = Calle.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        nombre = validated_data.get('nombre', None)
        self.validar_nombre(nombre, instance)

        if nombre:
            instance.nombre = nombre

        instance.save()
        return instance
