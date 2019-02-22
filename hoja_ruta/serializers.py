# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from contacto.models import ContactoNormalizado
from hoja_ruta.models import HojaRuta, DetalleHojaRuta, HistorialHojaRuta, Observacion, Producto, \
    ProductosDetalleHojaRuta
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
        cant_filas = 15
        barrio = instance
        calles_barrio = CallesBarrio.objects.filter(
            barrio=barrio
        ).order_by('calle__nombre')

        historial = HistorialHojaRuta()
        historial.owner = self.context['request'].user
        historial.barrio = barrio
        historial.save()

        for calle_barrio in calles_barrio:
            contactos = ContactoNormalizado.objects.filter(
                barrio=calle_barrio.barrio,
                calle=calle_barrio.calle,
                estado=ACTIVO
            ).extra(
                {'altura_int': "CAST(altura as UNSIGNED)"}
            ).order_by('altura_int')

            if len(contactos) > 0:
                paginator = Paginator(contactos, cant_filas)

                for page in range(1, paginator.num_pages + 1):
                    hoja_ruta = HojaRuta()
                    hoja_ruta.calle_barrio = calle_barrio
                    hoja_ruta.numero = HojaRuta.nextNumber()
                    hoja_ruta.historial = historial
                    hoja_ruta.save()

                    altura_desde = 0
                    altura_hasta = 0
                    cant_registros = 0
                    first = True

                    cont = 1
                    for contacto in paginator.page(page).object_list:
                        detalle = DetalleHojaRuta()
                        detalle.hoja_ruta = hoja_ruta
                        str_cont = str(cont)
                        detalle.numero_orden = str_cont if len(str_cont) > 1 else '0' + str_cont
                        detalle.tipo = contacto.tipo
                        detalle.titular = contacto.titular
                        detalle.save()

                        contacto_altura = None

                        try:
                            contacto_altura = int(contacto.altura)
                        except Exception:
                            pass

                        if first is True:
                            altura_desde = contacto_altura
                            altura_hasta = contacto_altura
                            first = False
                        else:
                            if contacto_altura > altura_hasta:
                                altura_hasta = contacto_altura

                            if contacto_altura < altura_desde:
                                altura_desde = contacto_altura

                        cant_registros=cont
                        cont += 1
                        detalle.save()
                    hoja_ruta.cant_registros = cant_registros
                    hoja_ruta.altura_desde = altura_desde
                    hoja_ruta.altura_hasta = altura_hasta
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


class DetalleHojaRutaSerializer(serializers.ModelSerializer):
    provincia=serializers.SerializerMethodField()
    localidad=serializers.SerializerMethodField()
    barrio=serializers.SerializerMethodField()
    calle=serializers.SerializerMethodField()
    producto=serializers.SerializerMethodField()
    observacion=serializers.SerializerMethodField()

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
            'producto',
            'observacion'

        )

    def get_provincia(self, obj):
        return obj.provincia.nombre

    def get_localidad(self, obj):
        return obj.localidad.nombre

    def get_barrio(self, obj):
        return obj.barrio.nombre

    def get_calle(self, obj):
        return obj.calle.nombre

    def get_producto(self, obj):

        if obj.detalle_productos.all().count() > 0:
            resutl = []

            detalle_productos = obj.detalle_productos.first()

            for prodcut in detalle_productos.producto.all():
                resutl.append({
                    'id': prodcut.id,
                    'nombre': prodcut.nombre
                })

            return resutl
        else:
            return None

    def get_observacion(self, obj):

        if obj.observacion:
            return {
                'id': obj.observacion.id,
                'nombre': obj.observacion.nombre
            }
        else:
            return None

    def update(self, instance, validated_data):
        try:
            observacion_id = self.initial_data['observacion']['id']

            if observacion_id:
                observacion=get_object_or_404(Observacion, id=observacion_id)

        except Exception:
            observacion=None

        try:
            producto_ids = self.initial_data['producto']

            list = []
            for ids in producto_ids:
                try:
                    id = ids['id']
                    producto= Producto.objects.get(id=id)
                    list.append(producto)
                except Exception:
                    pass

        except Exception:
            producto=None

        instance.observacion = None

        if observacion:
            instance.observacion=observacion

        if list:
            ProductosDetalleHojaRuta.objects.filter(detalle=instance).delete()
            productos=ProductosDetalleHojaRuta.objects.create(
                detalle=instance,
            )
            productos.producto.set(list)
            for produc in list:
                productos.producto.add(produc)
            producto.save()

        instance.save()
        return instance


class ActualizarHojaRutaSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        try:
            vendedor_id = self.initial_data['asignada_a']['id']
            vendedor=get_object_or_404(User, id=vendedor_id)
        except Exception:
            vendedor=None

        if vendedor:
            instance.asignada_a=vendedor

        instance.save()
        return instance


class ObservacionSerializer(serializers.ModelSerializer):

    class Meta:
        model=Observacion
        fields=(
            'id',
            'nombre',
        )


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
        )