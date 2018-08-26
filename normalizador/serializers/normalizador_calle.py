# -*- coding: utf-8 -*-
from rest_framework import serializers

from normalizador.models.calles_barrio import CallesBarrio
from normalizador.models.filtro_calle import FiltroCalle
from normalizador.serializers.filtro_calle import FiltroCalleSerializer


class NormalizadorCalleSerializer(serializers.Serializer):
    calle_barrio=serializers.SerializerMethodField()
    all=serializers.BooleanField(default=False)
    calles_mal=serializers.ListSerializer(
        child=serializers.IntegerField(min_value=0),
        default=[]
    )
    filtros=serializers.SerializerMethodField()


    class Meta:
        model = CallesBarrio
        fields = (
            'calle_barrio',
            'all',
            'calles_mal',
            'filtros'
        )

    def get_calle_barrio(self, obj):
        return obj.id

    def get_filtros(self, obj):
        fitros = FiltroCalle.objects.filter(calle_barrio=obj)
        return FiltroCalleSerializer(fitros, many=True).data
