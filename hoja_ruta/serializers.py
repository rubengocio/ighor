# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from rest_framework import serializers

from contacto.models import ContactoNormalizado
from hoja_ruta.models import HojaRuta, DetalleHojaRuta, HistorialHojaRuta
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.serializers.barrio import BarrioSerializer
from normalizador.serializers.calle import CalleSerializer


class GeneradorHojaRutaSerializer(serializers.ModelSerializer):
    historial=serializers.SerializerMethodField()

    class Meta:
        model=Barrio
        fields=(
            'historial',
        )

    def update(self, instance, validated_data):
        cant_filas=21
        barrio = instance
        calles_barrio=CallesBarrio.objects.filter(
            barrio=barrio
        ).order_by('calle__nombre')

        historial=HistorialHojaRuta()
        historial.owner=self.context['request'].user
        historial.barrio=barrio
        historial.save()

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
                hoja_ruta.historial=historial
                hoja_ruta.save()

                altura_desde=0
                altura_hasta=0
                cant_registros=0
                first=True

                cont=1
                for contacto in paginator.page(page).object_list:
                    detalle=DetalleHojaRuta()
                    detalle.hoja_ruta=hoja_ruta
                    str_cont=str(cont)
                    detalle.numero_orden=str_cont if len(str_cont) > 1 else '0' + str_cont
                    detalle.tipo=contacto.tipo
                    detalle.titular=contacto.titular
                    detalle.save()

                    if first is True:
                        altura_desde=contacto.altura
                        altura_hasta=contacto.altura
                        first=False
                    else:
                        if contacto.altura > altura_hasta:
                            altura_hasta=contacto.altura

                        if contacto.altura < altura_desde:
                            altura_desde=contacto.altura
                    cant_registros=cont
                    cont += 1
                hoja_ruta.cant_registros=cant_registros
                hoja_ruta.altura_desde=altura_desde
                hoja_ruta.altura_hasta=altura_hasta
                hoja_ruta.save()
        return instance


    def get_historial(self, obj):
        historial = HistorialHojaRuta.objects.filter(
            owner=self.context['request'].user
        ).order_by('-id').first()

        return HistorialHojaRutaSerializer(historial).data


class DetalleHojaRutaSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()
    titular = serializers.SerializerMethodField()
    apellido = serializers.SerializerMethodField()
    nombre = serializers.SerializerMethodField()
    provincia = serializers.SerializerMethodField()
    localidad = serializers.SerializerMethodField()
    barrio = serializers.SerializerMethodField()
    calle = serializers.SerializerMethodField()
    altura = serializers.SerializerMethodField()
    piso = serializers.SerializerMethodField()
    departamento = serializers.SerializerMethodField()
    observaciones = serializers.SerializerMethodField()


    class Meta:
        model=DetalleHojaRuta
        fields=(
            'id',
            'numero_orden',
            'tipo',
            'titular',
            'apellido',
            'nombre',
            'provincia',
            'localidad',
            'barrio',
            'calle',
            'altura',
            'piso',
            'departamento',
            'observaciones'
        )

    def get_tipo(self, obj):
        return obj.tipo

    def get_titular(self, obj):
        return obj.titular

    def get_apellido(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.apellido.strip()

    def get_nombre(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.nombre.strip()

    def get_provincia(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.provincia.nombre if contact.provincia else ''

    def get_localidad(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.localidad.nombre if contact.localidad else ''

    def get_barrio(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.barrio.nombre if contact.barrio else ''

    def get_calle(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.calle.nombre if contact.calle else ''

    def get_altura(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.altura.strip()

    def get_piso(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.piso.strip()

    def get_departamento(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.departamento.strip()

    def get_observaciones(self, obj):
        return ''



class HistorialHojaRutaSerializer(serializers.ModelSerializer):
    owner=serializers.SerializerMethodField()
    hojas=serializers.SerializerMethodField()
    barrio=BarrioSerializer()

    class Meta:
        model=HistorialHojaRuta
        fields=(
            'id',
            'fecha',
            'barrio',
            'owner',
            'hojas'
        )

    def get_owner(self, obj):
        return {
            'id': obj.owner.id,
            'first_name': obj.owner.first_name,
            'last_name':obj.owner.last_name,
            'email':obj.owner.email
        }

    def get_hojas(self, obj):
        hojas=obj.hojas_ruta.all()
        return HojaRutaSerializer(hojas, many=True).data


class HojaRutaSerializer(serializers.ModelSerializer):
    calle = serializers.SerializerMethodField()
    asignada_a=serializers.SerializerMethodField()
    estado=serializers.SerializerMethodField()

    class Meta:
        model=HojaRuta
        fields=(
            'id',
            'numero',
            'calle',
            'altura_desde',
            'altura_hasta',
            'cant_registros',
            'asignada_a',
            'estado'
        )

    def get_calle(self, obj):
        calle=CalleSerializer(obj.calle_barrio.calle).data
        return calle

    def get_asignada_a(self, obj):
        if obj.asignada_a:
            return {
                'id': obj.asignada_a.id,
                'first_name': obj.asignada_a.first_name,
                'last_name': obj.asignada_a.last_name,
                'email': obj.asignada_a.email
            }
        else:
            return None

    def get_estado(self, obj):
        return {
            'id': obj.estado,
            'nombre': obj.get_estado_display()
        }