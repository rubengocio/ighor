# -*- coding: utf-8 -*-
from rest_framework import serializers
from normalizador.models.barrio import Barrio
from normalizador.models.filtro_barrio import FiltroBarrio
from normalizador.serializers.filtro_barrio import FiltroBarrioSerializer


class NormalizadorBarrioSerializer(serializers.Serializer):
    barrio=serializers.SerializerMethodField()
    all=serializers.BooleanField(default=False)
    barrios_mal=serializers.ListSerializer(
        child=serializers.IntegerField(min_value=0),
        default=[]
    )
    filtros=serializers.SerializerMethodField()


    class Meta:
        model = Barrio
        fields = (
            'barrio',
            'all',
            'barrios_mal',
            'filtros'
        )

    def get_barrio(self, obj):
        return obj.id

    def get_filtros(self, obj):
        fitros = FiltroBarrio.objects.filter(barrio=obj)
        return FiltroBarrioSerializer(fitros, many=True).data
