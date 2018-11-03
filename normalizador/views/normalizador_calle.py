# -*- coding: utf-8 -*-
from django.db import connection
from django.db import transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from contacto.models import ContactoNormalizado
from normalizador.models import CalleIncorrecta
from normalizador.models import Criterio
from normalizador.models import DiccionarioCalle
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.models.filtro_calle import FiltroCalle
from normalizador.serializers.normalizador_calle import NormalizadorCalleSerializer



class NormalizadorCalleViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                GenericViewSet):

    queryset = CallesBarrio.objects.all()
    serializer_class = NormalizadorCalleSerializer
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

        calle_barrio = request.data.get('calle_barrio', None)
        calle_barrio = get_object_or_404(CallesBarrio, pk=calle_barrio)
        all = request.data.get('all', False)
        filtros = request.data.get('filtros', None)

        query = ' SELECT normalizador_calleincorrecta.id, '
        query += ' normalizador_calleincorrecta.nombre, '
        query += ' normalizador_calle.nombre as calle '
        query += ' FROM normalizador_calleincorrecta '
        query += ' INNER JOIN contacto_titular ON (contacto_titular.domicilio_calle=normalizador_calleincorrecta.nombre) '
        query += ' INNER JOIN contacto_contactonormalizado ON (contacto_contactonormalizado.tipo=contacto_titular.tipo AND contacto_contactonormalizado.titular=contacto_titular.titular AND contacto_contactonormalizado.barrio_id=%s) '
        query += ' LEFT JOIN normalizador_diccionariocalle ON (normalizador_diccionariocalle.calle_incorrecta_id=normalizador_calleincorrecta.id) '
        query += ' LEFT JOIN normalizador_callesbarrio ON (normalizador_callesbarrio.id=normalizador_diccionariocalle.calle_barrio_id) '
        query += ' LEFT JOIN normalizador_calle ON (normalizador_calle.id=normalizador_callesbarrio.calle_id) '
        query += ' where 1=1 '

        query = query % calle_barrio.barrio.id

        if all is False:
            query += ' and normalizador_diccionariocalle.calle_barrio_id is null '

        filters = ''
        for item in filtros:
            criterio = get_object_or_404(Criterio, pk=item.get('criterio', None))
            filters += u" %s %s normalizador_calleincorrecta.nombre %s '%s' %s" % (
                u' AND ' if item.get('operador', None) == 1 else u' OR ',
                u'(' if item.get('parentesis_abierto', False) == True else '',
                criterio.valor,
                item.get('valor', ''),
                u')' if item.get('parentesis_cerrado', False) == True else '',
            )

        if len(filters) > 0:
            query += filters

        query += ' group by normalizador_calleincorrecta.id, normalizador_calleincorrecta.nombre, normalizador_calle.nombre '
        query += ' order by normalizador_calleincorrecta.nombre '

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
                'calle': row[2]
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

        calle_barrio = self.get_object()
        calles_mal = request.data.get('calles_mal', None)
        filtros = request.data.get('filtros', None)
        cant=0
        try:
            with transaction.atomic():
                FiltroCalle.objects.filter(calle_barrio=calle_barrio).delete()
                for item in filtros:
                    criterio = get_object_or_404(Criterio, pk=item.get('criterio', None))
                    FiltroCalle.objects.create(
                        calle_barrio=calle_barrio,
                        operador=item.get('operador', None),
                        parentesis_abierto=item.get('parentesis_abierto', None),
                        criterio=criterio,
                        valor=item.get('valor', None),
                        parentesis_cerrado=item.get('parentesis_cerrado', None)
                    )

                calles_incorrectas=CalleIncorrecta.objects.filter(id__in=calles_mal)
                diccionario_calles=[]
                for calle_incorrecta in calles_incorrectas:
                    if not DiccionarioCalle.objects.filter(calle_incorrecta=calle_incorrecta,calle_barrio=calle_barrio).exists():
                        diccionario_calles.append(
                            DiccionarioCalle.objects.create(
                                calle_incorrecta=calle_incorrecta,
                                calle_barrio=calle_barrio
                            )
                        )
                    else:
                        diccionario_calles.append(
                            DiccionarioCalle.objects.filter(
                                calle_incorrecta=calle_incorrecta,
                                calle_barrio=calle_barrio
                            ).first()
                        )
                    cant += 1

                cant_filas=ContactoNormalizado.actualizar_calle(diccionario_calles, calle_barrio)
        except Exception as ex:
            print(ex)
            pass

        response={
            'cant_filas': cant
        }
        return Response(response, status=status.HTTP_201_CREATED)