# -*- coding: utf-8 -*-
from django.db import connection
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from contacto.models import ContactoNormalizado
from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio
from normalizador.models.calles_barrio import CallesBarrio


class ReporteNormalizacionBarrioAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        "cantidad_registros_diccionario": cantidad total de registros en el diccionario de barrios,
        "cantidad_registros_normalizados_diccionario": cantidad de registros normalizados en el diccionario de barrios,
        "cantidad_registros_normalizados_por_sector_diccionario": cantidad de registros normalizados del sector en el diccionario de barrios,
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        barrio_id=str(instance.id)
        cuadrante_id=str(instance.cuadrante.id)

        query = "  select count(*) as total_registros, "
        query += " 	    count(case when normalizador_diccionariobarrio.barrio_id is null then null else normalizador_diccionariobarrio.barrio_id end) as cant_barrio_normalizado, "
        query += " 	    count(case when normalizador_barrio.cuadrante_id = " + cuadrante_id + " then normalizador_diccionariobarrio.barrio_id else null end) as cant_barrios_por_sector "
        query += " from normalizador_diccionariobarrio  "
        query += " left join normalizador_barrio on normalizador_barrio.id = normalizador_diccionariobarrio.barrio_id "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_diccionario': rows[0][0],
            'cantidad_registros_normalizados_diccionario': rows[0][1],
            'cantidad_registros_normalizados_por_sector_diccionario': rows[0][2],
        }

        return Response(result, status=status.HTTP_200_OK)


class ReporteNormalizacionCallesBarrioAPIView(generics.RetrieveAPIView):
    """
    Devuelve un objeto con las cantidades de registros normalizados

        "cantidad_registros_diccionario": cantidad total de registros en el diccionario de calles
	    "cantidad_registros_normalizados_diccionario": cantidad de registros normalizados en el diccionario de calles
	    "cantidad_registros_normalizados_por_barrio_diccionario": cantidad de registros normalizados del barrio en el diccionario de calles

    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CallesBarrio.objects.filter(
        barrio__estado=ACTIVO,
        barrio__cuadrante__estado=ACTIVO
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        calle_id = str(instance.calle.id)
        barrio_id = str(instance.barrio.id)

        query = " select count(*) as  total_registros, "
        query += " 	    count(case when normalizador_diccionariocalle.calle_barrio_id is null then null else normalizador_diccionariocalle.calle_barrio_id end) as cant_calle_normalizado, "
        query += " 	    count(case when normalizador_callesbarrio.barrio_id = " + barrio_id + " then normalizador_diccionariocalle.calle_barrio_id else null end) as cant_calles_por_sector "
        query += " from normalizador_calleincorrecta  "
        query += "  left join normalizador_diccionariocalle on normalizador_diccionariocalle.calle_incorrecta_id = normalizador_calleincorrecta.id "
        query += "  left join normalizador_callesbarrio on normalizador_callesbarrio .id = normalizador_diccionariocalle.calle_barrio_id "

        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = {
            'cantidad_registros_diccionario': rows[0][0],
            'cantidad_registros_normalizados_diccionario': rows[0][1],
            'cantidad_registros_normalizados_por_barrio_diccionario': rows[0][2],
        }

        return Response(result, status=status.HTTP_200_OK)


class ReporteContactosNormalizadosListAPIView(generics.ListAPIView):
    """
        Devuelve un listado de objetos con las cantidades de contactos normalizados

        "nombre": provincia, localidad, cuadrante, barrio o ciudad (Segun lo seleccionado)
	    "cantidad_no_clientes": cantidad de contactos normalizados que no son clientes
	    "cantidad_clientes": cantidad de contactos normalizados que son clientes
	    "cantidad_total": cantidad total de contactos normalizados

	    filtros:
	        provincia: id de provincia
	        localidad: id de localidad
	        cuadrante: id de cuadrante
	        barrio: id de barrio

	    ejemplos:
	        http://localhost:8000/v1/reporte_contactos_normalizados/?provincia=4
	        http://localhost:8000/v1/reporte_contactos_normalizados/?localidad=4618
	        http://localhost:8000/v1/reporte_contactos_normalizados/?cuadrante=19
	        http://localhost:8000/v1/reporte_contactos_normalizados/?barrio=20

	    respuesta:
	        {
                "result": [
                    {
                        "cantidad_total": 34,
                        "nombre": "CORDOBA",
                        "cantidad_clientes": 20,
                        "cantidad_no_clientes": 14
                    }
                ]
            }
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = []

        provincia = request.GET.get('provincia', None)
        localidad = request.GET.get('localidad', None)
        cuadrante = request.GET.get('cuadrante', None)
        barrio = request.GET.get('barrio', None)

        columna = ""
        where = ""

        if barrio:
            columna = " normalizador_calle.nombre "
            where = " where normalizador_barrio.id = {} ".format(barrio)
        elif cuadrante:
            columna = " normalizador_barrio.nombre "
            where = " where normalizador_cuadrante.id = {} ".format(cuadrante)
        elif localidad:
            columna = " normalizador_cuadrante.nombre "
            where = " where normalizador_localidad.id = {} ".format(localidad)
        elif provincia:
            columna = " normalizador_localidad.nombre "
            where = " where normalizador_provincia.id = {} ".format(provincia)
        else:
            columna = " normalizador_provincia.nombre "

        query = " select {} , ".format(columna)
        query += " count(case when contacto_clientejk.id is null then contacto_contactonormalizado.id else null end) as cantidad_no_clientes, "
        query += " count(contacto_clientejk.id) as cantidad_clientes, "
        query += " count(*) as cantidad_total "
        query += " from contacto_contactonormalizado "
        query += " inner join normalizador_provincia on normalizador_provincia.id = contacto_contactonormalizado.provincia_id "
        query += " inner join normalizador_localidad on normalizador_localidad.id = contacto_contactonormalizado.localidad_id "
        query += " inner join normalizador_barrio on normalizador_barrio.id = contacto_contactonormalizado.barrio_id "
        query += " inner join normalizador_calle on normalizador_calle.id = contacto_contactonormalizado.calle_id "
        query += " inner join normalizador_cuadrante on normalizador_cuadrante.id = normalizador_barrio.cuadrante_id "
        query += " left join contacto_clientejk on contacto_clientejk.nro_documento = contacto_contactonormalizado.titular and contacto_clientejk.tipo_documento = contacto_contactonormalizado.tipo "
        query += where
        query += " group by {} ".format(columna)
        query += " order by {} ".format(columna)

        rows = []
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as ex:
            pass
        finally:
            cursor.close()

        for row in rows:
            data.append({
                'nombre': row[0],
                'cantidad_no_clientes': row[1],
                'cantidad_clientes': row[2],
                'cantidad_total': row[3]
            })

        return Response({'result': data})


class ReporteObservacionesPorVendedorListAPIView(generics.ListAPIView):
    """
        Devuelve un listado de objetos con las cantidades de observaciones

        "id": id de observacion
        "nombre": nombre de observacion
        "cantidad": cantidad de observaciones

        filtros:
            vendedor: id de vendedor
            fecha_desde: fecha desde
            fecha_hasta: fecha hasta

        ejemplos:
            http://localhost:8000/v1/reporte_observaciones_vendedor/
            http://localhost:8000/v1/reporte_observaciones_vendedor/?vendedor=1
            http://localhost:8000/v1/reporte_observaciones_vendedor/?fecha_desde=2019-01-01
            http://localhost:8000/v1/reporte_observaciones_vendedor/?fecha_hasta=2019-12-31
            http://localhost:8000/v1/reporte_observaciones_vendedor/?fecha_desde=2019-01-01&fecha_hasta=2019-12-31
            http://localhost:8000/v1/reporte_observaciones_vendedor/?vendedor=1&fecha_desde=2019-01-01&fecha_hasta=2019-12-31

        respuesta:
            {
                "result": [
                    {
                        "nombre": "Cliente fallecido",
                        "id": 3,
                        "cantidad": 0
                    },
                    {
                        "nombre": "No tiene tarjeta",
                        "id": 2,
                        "cantidad": 0
                    },
                    {
                        "nombre": "No vive más alli",
                        "id": 1,
                        "cantidad": 0
                    }
                ]
            }
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = []

        vendedor = request.GET.get('vendedor', None)
        fecha_desde = request.GET.get('fecha_desde', None)
        fecha_hasta = request.GET.get('fecha_hasta', None)

        where = " "

        if vendedor:
            where += " and hoja_ruta_hojaruta.asignada_a_id = {} ".format(vendedor)

        if fecha_desde:
            where += " and date(hoja_ruta_hojaruta.fecha) >= '{}' ".format(fecha_desde)

        if fecha_hasta:
            where += " and date(hoja_ruta_hojaruta.fecha) <= '{}' ".format(fecha_hasta)

        query = " select hoja_ruta_observacion.id,  "
        query += "       hoja_ruta_observacion.nombre, "
        query += "       (case when x.cantidad is null then 0 else x.cantidad end) as cantidad "
        query += " from hoja_ruta_observacion "
        query += " left join (select hoja_ruta_detallehojaruta.observacion_id, "
        query += "                  count(*) as cantidad "
        query += "              from hoja_ruta_hojaruta "
        query += "              inner join hoja_ruta_detallehojaruta on hoja_ruta_detallehojaruta.hoja_ruta_id = hoja_ruta_hojaruta.id "
        query += "              where hoja_ruta_detallehojaruta.observacion_id is not null "
        query += where
        query += "              group by hoja_ruta_detallehojaruta.observacion_id) as x on x.observacion_id = hoja_ruta_observacion.id "
        query += " order by hoja_ruta_observacion.nombre "

        rows = []
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as ex:
            pass
        finally:
            cursor.close()

        for row in rows:
            data.append({
                'id': row[0],
                'nombre': row[1],
                'cantidad': row[2],
            })

        return Response({'result': data})
