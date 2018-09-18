# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from normalizador.enum import ACTIVO
from normalizador.models.barrio import Barrio


class HojaRutaRetrieveAPIView(generics.RetrieveAPIView):
    """
     Listado de cuadrantes de una localidad
    """

    queryset = Barrio.objects.filter(
        estado=ACTIVO,
        cuadrante__estado=ACTIVO
    )
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()


        return Response({'data':'ok'})


"""
select contacto_titular.nombre,
		contacto_titular.apellido,
		normalizador_calle.nombre,
		contacto_contactonormalizado.altura,
		contacto_contactonormalizado.piso,
		contacto_contactonormalizado.departamento,
		normalizador_barrio.nombre,
		contacto_titular.telefono,
		contacto_cliente.productos,
		contacto_cliente.cualidad,
		contacto_cliente.meses_deuda,
		contacto_cliente.monto_deuda,
		contacto_cliente.inhumados,
		contacto_titular.titular,
		contacto_titular.estado,
		contacto_titular.tipo,
		contacto_titular.tipo_cuenta,
		contacto_contactonormalizado.observaciones
from contacto_contactonormalizado
inner join contacto_titular on (contacto_titular.tipo=contacto_contactonormalizado.tipo and contacto_titular.titular=contacto_contactonormalizado.titular)
inner join normalizador_provincia on (normalizador_provincia.id=contacto_contactonormalizado.provincia_id)
inner join normalizador_barrio on (normalizador_barrio.id=contacto_contactonormalizado.barrio_id)
inner join normalizador_calle on (normalizador_calle.id=contacto_contactonormalizado.calle_id)
left join contacto_cliente on (contacto_cliente.numero_documento=contacto_contactonormalizado.titular);
"""