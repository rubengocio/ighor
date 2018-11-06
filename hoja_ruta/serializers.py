# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from rest_framework import serializers

from contacto.models import ContactoNormalizado
from hoja_ruta.models import HojaRuta, DetalleHojaRuta
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.calle import CalleSerializer


class GeneradorHojaRutaSerializer(serializers.ModelSerializer):
    hojas=serializers.SerializerMethodField()

    class Meta:
        model=Barrio
        fields=(
            'hojas',
        )

    def update(self, instance, validated_data):
        cant_filas=21
        barrio = instance
        calles_barrio=CallesBarrio.objects.filter(
            barrio=barrio
        ).order_by('calle__nombre')

        for calle_barrio in calles_barrio:
            contactos=ContactoNormalizado.objects.filter(
                barrio=calle_barrio.barrio,
                calle=calle_barrio.calle,
                estado=ACTIVO
            ).extra(
                {'altura_int': "CAST(altura as UNSIGNED)"}
            ).order_by('altura_int')

            if len(contactos) == 0:
                break

            paginator = Paginator(contactos, cant_filas)

            for page in range(1, paginator.num_pages + 1):
                hoja_ruta=HojaRuta()
                hoja_ruta.calle_barrio=calle_barrio
                hoja_ruta.numero=HojaRuta.nextNumber()
                hoja_ruta.save()

                cont=1
                for contacto in paginator.page(page).object_list:
                    detalle=DetalleHojaRuta()
                    detalle.hoja_ruta=hoja_ruta
                    str_cont=str(cont)
                    detalle.numero_orden=str_cont if len(str_cont) > 1 else '0' + str_cont
                    detalle.tipo=contacto.tipo
                    detalle.titular=contacto.titular
                    detalle.save()
                    cont += 1

        return instance

    def get_hojas(self, obj):
        hojas=HojaRuta.objects.filter(
            calle_barrio__barrio=obj
        )
        return HojaRutaSerializer(hojas, many=True).data


class HojaRutaSerializer(serializers.ModelSerializer):
    calle = serializers.SerializerMethodField()

    class Meta:
        model=HojaRuta
        fields=(
            'id',
            'numero',
            'calle',
        )

    def get_calle(self, obj):
        calle=CalleSerializer(obj.calle_barrio.calle).data
        return calle





