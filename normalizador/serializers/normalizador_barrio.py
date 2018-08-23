# -*- coding: utf-8 -*-
from django.db import transaction, connection
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from normalizador.models import Criterio
from normalizador.models import DiccionarioBarrio
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


    def update(self, instance, validated_data):
        barrio = self.initial_data.get('barrio', None)
        barrio = get_object_or_404(Barrio, pk=barrio)
        all = self.initial_data.get('all', None)
        barrios_mal = self.initial_data.get('barrios_mal', None)
        filtros = self.initial_data.get('filtros', None)

        try:
            with transaction.atomic():
                FiltroBarrio.objects.filter(barrio=barrio).delete()
                for item in filtros:
                    FiltroBarrio.objects.create(
                        barrio=barrio,
                        operador=item.get('operador', None),
                        parentesis_abierto=item.get('parentesis_abierto', None),
                        criterio=item.get('criterio', None),
                        valor=item.get('valor', None),
                        parentesis_cerrado=item.get('parentesis_cerrado', None)
                    )
        except Exception:
            pass

        return barrio