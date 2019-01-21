# -*- coding: utf-8 -*-
from django.conf.urls import url

from hoja_ruta.views import GenerarHojaRutaUpdateAPIView, BarrioHojaRutaRetrieveAPIView, HojaRutaRetrieveUpdateAPIView, \
    Pdf, ActualizarHojaRutaCreateAPIView, DetalleHojaRutaVendedorListCreateAPIView, ObservacionViewSet, ProductoViewSet
from user.views import VendedorListAPIView, VendedorRetrieveAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'observacion', ObservacionViewSet)
router.register(r'producto', ProductoViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^barrio/(?P<pk>[0-9]+)/generar_hoja_ruta/$', GenerarHojaRutaUpdateAPIView.as_view()),
    url(r'^barrio/(?P<pk>[0-9]+)/hojas_ruta/$', BarrioHojaRutaRetrieveAPIView.as_view()),
    url(r'^hoja_ruta/(?P<pk>[0-9]+)/$', HojaRutaRetrieveUpdateAPIView.as_view()),
    url(r'^vendedor_detalle_hoja_ruta/$', DetalleHojaRutaVendedorListCreateAPIView.as_view()),
    url(r'^actualizar_hoja_ruta/$', ActualizarHojaRutaCreateAPIView.as_view()),
    url(r'^vendedor/$', VendedorListAPIView.as_view()),
    url(r'^vendedor/(?P<pk>[0-9]+)/$', VendedorRetrieveAPIView.as_view()),
    url(r'^pdf/$', Pdf.as_view())
]


