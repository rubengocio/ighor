# -*- coding: utf-8 -*-
from django.db import connection
from django.db import transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from contacto.models import ContactoNormalizado
from normalizador.models import Criterio
from normalizador.models import DiccionarioBarrio
from normalizador.models.barrio import Barrio
from normalizador.models.filtro_barrio import FiltroBarrio
from normalizador.serializers.normalizador_barrio import NormalizadorBarrioSerializer
from normalizador.tasks import actualizar_calle_incorrecta


class NormalizadorBarrioViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                GenericViewSet):

    queryset = Barrio.objects.all()
    serializer_class = NormalizadorBarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
            Lista los filtros guardados para el barrio ingresado
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
            Retorna un listado de barrios mal escritos cargados en el diccionario de barrios filtrados segun los criterios ingresados en el body

                barrio: id de barrio seleccionado.

                all: true si se desea que se incluya en el listado los datos que ya tienen asignado un barrio. false si no se desea incluirlos.

                barrios_mal: array de ids de barrios mal que se desean actualizar.

                filtros: array de criterios de busqueda.

                    operador: 0 o 1 para (OR o AND)

                    parentesis_abierto: true si hay un prentesis abierto, false si no.

                    criterio: 1 (Like), 2 (Not Like), 3 (=), 4 (<>)

                    valor: texto de busqueda

                    parentesis_cerrado: true si hay un prentesis abierto, false si no.

        """

        barrio = request.data.get('barrio', None)
        barrio = get_object_or_404(Barrio, pk=barrio)
        all = request.data.get('all', False)
        barrios_mal = request.data.get('barrios_mal', None)
        filtros = request.data.get('filtros', None)

        query = ' select normalizador_diccionariobarrio.id, '
        query += ' normalizador_diccionariobarrio.nombre, '
        query += ' normalizador_barrio.nombre as barrio '
        query += ' from normalizador_diccionariobarrio '
        query += ' left join normalizador_barrio on normalizador_barrio.id = normalizador_diccionariobarrio.barrio_id '
        query += ' where 1=1 '

        if all is False:
            query += ' and barrio_id is null '

        filters = ''
        for item in filtros:
            criterio = get_object_or_404(Criterio, pk=item.get('criterio', None))
            filters += u" %s %s normalizador_diccionariobarrio.nombre %s '%s' %s" % (
                u' AND ' if item.get('operador', None) == 1 else u' OR ',
                u'(' if item.get('parentesis_abierto', False) == True else '',
                criterio.valor,
                item.get('valor', ''),
                u')' if item.get('parentesis_cerrado', False) == True else '',
            )

        if len(filters) > 0:
            query += filters

        query += ' order by normalizador_diccionariobarrio.nombre '

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as ex:
            rows=[]

        result=[]
        for row in rows:
            result.append({
                'id': row[0],
                'nombre': row[1],
                'barrio': row[2]
            })

        return Response(result, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        """
            Actualiza el barrio del diccionario de barrios para los valores ingresados y devuelve la cantidad de registros actualizados.
            Ademas guarda la los filtros ingresados para poder usarlos nuevamente.

                barrio: id de barrio seleccionado.

                all: true si se desea que se incluya en el listado los datos que ya tienen asignado un barrio. false si no se desea incluirlos.

                barrios_mal: array de ids de barrios mal que se desean actualizar.

                filtros: array de criterios de busqueda.

                    operador: 0 o 1 para (OR o AND)

                    parentesis_abierto: true si hay un prentesis abierto, false si no.

                    criterio: 1 (Like), 2 (Not Like), 3 (=), 4 (<>)

                    valor: texto de busqueda

                    parentesis_cerrado: true si hay un prentesis abierto, false si no.

        """

        barrio = self.get_object()
        barrios_mal = request.data.get('barrios_mal', None)
        filtros = request.data.get('filtros', None)
        cant_filas=0
        try:
            with transaction.atomic():
                FiltroBarrio.objects.filter(barrio=barrio).delete()
                for item in filtros:
                    criterio = get_object_or_404(Criterio, pk=item.get('criterio', None))
                    FiltroBarrio.objects.create(
                        barrio=barrio,
                        operador=item.get('operador', None),
                        parentesis_abierto=item.get('parentesis_abierto', None),
                        criterio=criterio,
                        valor=item.get('valor', None),
                        parentesis_cerrado=item.get('parentesis_cerrado', None)
                    )

                diccionario_barrios=DiccionarioBarrio.objects.filter(id__in=barrios_mal)
                for dicccionario in diccionario_barrios:
                    dicccionario.barrio=barrio
                    dicccionario.save()

                cant_filas=ContactoNormalizado.actualizar_barrio(diccionario_barrios, barrio)

                actualizar_calle_incorrecta(barrio.id)
        except Exception as ex:
            print(ex)
            pass

        response={
            'cant_filas':cant_filas
        }
        return Response(response, status=status.HTTP_201_CREATED)

