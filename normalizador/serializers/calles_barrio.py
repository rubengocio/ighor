# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador import constants
from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.barrio import BarrioSerializer
from normalizador.serializers.calle import CalleSerializer


class CallesBarrioSerializer(serializers.ModelSerializer):
    barrio = BarrioSerializer()
    calle = CalleSerializer()
    tipo_numeracion=serializers.SerializerMethodField()

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
            'tipo_numeracion',
            'nomenclado'
        )

    def validar_calle_barrio(self, barrio, calle, instance=None):
        calles_barrio=CallesBarrio.objects.filter(
            barrio=barrio,
            calle=calle
        )

        if instance:
            calles_barrio=calles_barrio.exclude(id=instance.id)

        if calles_barrio.exists():
            raise serializers.ValidationError({'non_field_errors': [constants.CALLE_BARRIO_EXISTE]})

    def get_tipo_numeracion(self, obj):
        return {
            'id': obj.tipo_numeracion,
            'nombre': obj.get_tipo_numeracion_display()
        }

    def create(self, validated_data):
        id_barrio = self.initial_data.get('barrio').get('id', None)
        id_calle = self.initial_data.get('calle').get('id', None)
        id_tipo_numeracion = self.initial_data.get('tipo_numeracion').get('id', None)

        barrio = Barrio.objects.filter(pk=id_barrio).first()
        calle = Calle.objects.filter(pk=id_calle).first()

        if not id_barrio:
            raise serializers.ValidationError({'barrio': [constants.CAMPO_REQUERIDO]})
        elif not barrio:
            raise serializers.ValidationError({'barrio': [constants.BARRIO_NO_EXISTE]})

        if not id_calle:
            raise serializers.ValidationError({'calle': [constants.CAMPO_REQUERIDO]})
        elif not calle:
            raise serializers.ValidationError({'calle': [constants.CALLE_NO_EXISTE]})

        if not id_tipo_numeracion:
            raise serializers.ValidationError({'tipo_numeracion': [constants.CAMPO_REQUERIDO]})

        self.validar_calle_barrio(barrio, calle)

        validated_data['barrio'] = barrio
        validated_data['calle'] = calle
        validated_data['tipo_numeracion'] = id_tipo_numeracion

        instance = CallesBarrio.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        id_barrio = self.initial_data.get('barrio').get('id', None)
        id_calle = self.initial_data.get('calle').get('id', None)
        id_tipo_numeracion = self.initial_data.get('tipo_numeracion').get('id', None)

        altura_desde = validated_data.get('altura_desde', None)
        altura_hasta = validated_data.get('altura_hasta', None)
        referencia = validated_data.get('referencia', None)
        plano = validated_data.get('plano', None)
        ubicacion = validated_data.get('ubicacion', None)

        barrio = Barrio.objects.filter(pk=id_barrio).first()
        calle = Calle.objects.filter(pk=id_calle).first()

        if not id_barrio:
            raise serializers.ValidationError({'barrio': [constants.CAMPO_REQUERIDO]})
        elif not barrio:
            raise serializers.ValidationError({'barrio': [constants.BARRIO_NO_EXISTE]})

        if not id_calle:
            raise serializers.ValidationError({'calle': [constants.CAMPO_REQUERIDO]})
        elif not calle:
            raise serializers.ValidationError({'calle': [constants.CALLE_NO_EXISTE]})

        if not id_tipo_numeracion:
            raise serializers.ValidationError({'tipo_numeracion': [constants.CAMPO_REQUERIDO]})

        self.validar_calle_barrio(barrio, calle, instance)

        if barrio:
            instance.barrio = barrio

        if calle:
            instance.calle = calle

        if altura_desde:
            instance.altura_desde = altura_desde

        if altura_hasta:
            instance.altura_hasta = altura_hasta

        if referencia:
            instance.referencia = referencia

        if plano:
            instance.plano = plano

        if ubicacion:
            instance.ubicacion = ubicacion

        if id_tipo_numeracion:
            instance.tipo_numeracion=id_tipo_numeracion

        instance.save()
        return instance


class CallesBarrioSimpleSerializer(serializers.ModelSerializer):
    calle = CalleSerializer()

    class Meta:
        model = CallesBarrio
        fields = (
            'id',
            'calle',
            'altura_desde',
            'altura_hasta',
            'referencia',
            'plano',
            'ubicacion',
            'nomenclado'
        )