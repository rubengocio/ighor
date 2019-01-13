# -*- coding: utf-8 -*-
from django.conf.urls import url

from hoja_ruta.views import GenerarHojaRutaUpdateAPIView, BarrioHojaRutaRetrieveAPIView, HojaRutaRetrieveUpdateAPIView, \
    Pdf, ActualizarHojaRutaCreateAPIView
from user.views import VendedorListAPIView, VendedorRetrieveAPIView

urlpatterns = [
    url(r'^barrio/(?P<pk>[0-9]+)/generar_hoja_ruta/$', GenerarHojaRutaUpdateAPIView.as_view()),
    url(r'^barrio/(?P<pk>[0-9]+)/hojas_ruta/$', BarrioHojaRutaRetrieveAPIView.as_view()),
    url(r'^hoja_ruta/(?P<pk>[0-9]+)/$', HojaRutaRetrieveUpdateAPIView.as_view()),
    url(r'^hoja_ruta/$', ActualizarHojaRutaCreateAPIView.as_view()),
    url(r'^vendedor/$', VendedorListAPIView.as_view()),
    url(r'^vendedor/(?P<pk>[0-9]+)/$', VendedorRetrieveAPIView.as_view()),
    url(r'^pdf/$', Pdf.as_view())
]


