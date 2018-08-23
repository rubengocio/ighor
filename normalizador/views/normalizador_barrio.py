# -*- coding: utf-8 -*-
from django.db import connection
from django.db import transaction
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from normalizador.models import Criterio
from normalizador.models import DiccionarioBarrio
from normalizador.models.barrio import Barrio
from normalizador.models.filtro_barrio import FiltroBarrio
from normalizador.serializers.normalizador_barrio import NormalizadorBarrioSerializer


class NormalizadorBarrioViewSet(viewsets.ModelViewSet):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Barrio.objects.all()
    serializer_class = NormalizadorBarrioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        barrio = request.data.get('barrio', None)
        barrio = get_object_or_404(Barrio, pk=barrio)
        all = request.data.get('all', False)
        barrios_mal = request.data.get('barrios_mal', None)
        filtros = request.data.get('filtros', None)

        query = ' select id, '
        query += ' nombre, '
        #query += ' barrio_id '
        query += ' from normalizador_diccionariobarrio '
        query += ' where 1=1 '

        if all is False:
            query += ' and barrio_id is null '

        filters = ''
        for item in filtros:
            criterio = get_object_or_404(Criterio, pk=item.get('criterio', None))
            filters += u" %s %s nombre %s '%s' %s" % (
                u' AND ' if item.get('operador', None) == 1 else u' OR ',
                u'(' if item.get('parentesis_abierto', False) == True else '',
                criterio.valor,
                item.get('valor', ''),
                u'(' if item.get('parentesis_cerrado', False) == True else '',
            )

        if len(filters) > 0:
            query += filters

        query += ' order by nombre'

        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchall()

        return Response(row, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        barrio = self.get_object()
        barrios_mal = request.data.get('barrios_mal', None)
        filtros = request.data.get('filtros', None)

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

        except Exception:
            pass

        response={
            'cant_filas':diccionario_barrios.count()
        }
        return Response(response, status=status.HTTP_201_CREATED)