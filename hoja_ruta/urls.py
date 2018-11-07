# -*- coding: utf-8 -*-
from django.conf.urls import url

from hoja_ruta.views import GenerarHojaRutaUpdateAPIView, BarrioHojaRutaRetrieveAPIView, HojaRutaRetrieveAPIView

urlpatterns = [
    url(r'^barrio/(?P<pk>[0-9]+)/generar_hoja_ruta/$', GenerarHojaRutaUpdateAPIView.as_view()),
    url(r'^barrio/(?P<pk>[0-9]+)/hojas_ruta/$', BarrioHojaRutaRetrieveAPIView.as_view()),
    url(r'^hoja_ruta/(?P<pk>[0-9]+)/$', HojaRutaRetrieveAPIView.as_view()),
]


