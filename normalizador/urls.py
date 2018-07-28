# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework import routers

from normalizador.views.barrio import BarrioViewSet, BarrioCallesRetrieveAPIView
from normalizador.views.cuadrante import CuadranteViewSet, CuadranteBarriosRetrieveAPIView
from normalizador.views.localidad import LocalidadViewSet, LocalidadCuadrantesRetrieveAPIView
from normalizador.views.provincia import ProvinciaViewSet, ProvinciaLocalidadesRetrieveAPIView


router = routers.DefaultRouter()
router.register(r'provincia', ProvinciaViewSet)
router.register(r'localidad', LocalidadViewSet)
router.register(r'cuadrante', CuadranteViewSet)
router.register(r'barrio', BarrioViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^provincia/(?P<pk>[0-9]+)/localidades/$', ProvinciaLocalidadesRetrieveAPIView.as_view()),
    url(r'^localidad/(?P<pk>[0-9]+)/cuadrantes/$', LocalidadCuadrantesRetrieveAPIView.as_view()),
    url(r'^cuadrante/(?P<pk>[0-9]+)/barrios/$', CuadranteBarriosRetrieveAPIView.as_view()),
    url(r'^barrio/(?P<pk>[0-9]+)/calles/$', BarrioCallesRetrieveAPIView.as_view())
]


