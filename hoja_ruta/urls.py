# -*- coding: utf-8 -*-
from django.conf.urls import url

from hoja_ruta.views import GenerarHojaRutaUpdateAPIView

urlpatterns = [
    url(r'^barrio/(?P<pk>[0-9]+)/generar_hoja_ruta/$', GenerarHojaRutaUpdateAPIView.as_view()),
]


