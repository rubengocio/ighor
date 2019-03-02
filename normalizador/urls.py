# -*- coding: utf-8 -*-
from django.conf.urls import url
from rest_framework import routers

from normalizador.views.barrio import BarrioViewSet
from normalizador.views.calle import CalleViewSet
from normalizador.views.calles_barrio import BarrioCallesListAPIView, CallesBarrioViewSet
from normalizador.views.cuadrante import CuadranteViewSet, CuadranteBarriosRetrieveAPIView
from normalizador.views.localidad import LocalidadViewSet, LocalidadCuadrantesRetrieveAPIView
from normalizador.views.normalizador_barrio import NormalizadorBarrioViewSet
from normalizador.views.normalizador_calle import NormalizadorCalleViewSet
from normalizador.views.provincia import ProvinciaViewSet, ProvinciaLocalidadesRetrieveAPIView
from normalizador.views.reporte import ReporteNormalizacionBarrioAPIView, ReporteNormalizacionCallesBarrioAPIView, \
    ReporteContactosNormalizadosListAPIView, ReporteObservacionesPorVendedorListAPIView, \
    ReporteObservacionesPorMesListAPIView, ReporteVendedoresPorObservacionListAPIView

router = routers.DefaultRouter()
router.register(r'provincia', ProvinciaViewSet)
router.register(r'localidad', LocalidadViewSet)
router.register(r'cuadrante', CuadranteViewSet)
router.register(r'barrio', BarrioViewSet)
router.register(r'calle', CalleViewSet)
router.register(r'barrio_calle', CallesBarrioViewSet)
router.register(r'normalizadorbarrio', NormalizadorBarrioViewSet)
router.register(r'normalizadorcalle', NormalizadorCalleViewSet)


urlpatterns = router.urls

urlpatterns += [
    url(r'^provincia/(?P<pk>[0-9]+)/localidades/$', ProvinciaLocalidadesRetrieveAPIView.as_view()),
    url(r'^localidad/(?P<pk>[0-9]+)/cuadrantes/$', LocalidadCuadrantesRetrieveAPIView.as_view()),
    url(r'^cuadrante/(?P<pk>[0-9]+)/barrios/$', CuadranteBarriosRetrieveAPIView.as_view()),
    url(r'^barrio/(?P<pk>[0-9]+)/calles/$', BarrioCallesListAPIView.as_view()),
    url(r'^reporte_normalizacion_barrio/(?P<pk>[0-9]+)/$', ReporteNormalizacionBarrioAPIView.as_view()),
    url(r'^reporte_normalizacion_calle_barrio/(?P<pk>[0-9]+)/$', ReporteNormalizacionCallesBarrioAPIView.as_view()),
    url(r'^reporte_contactos_normalizados/$', ReporteContactosNormalizadosListAPIView.as_view()),
    url(r'^reporte_observaciones_vendedor/$', ReporteObservacionesPorVendedorListAPIView.as_view()),
    url(r'^reporte_observaciones_mes/$', ReporteObservacionesPorMesListAPIView.as_view()),
    url(r'^reporte_vendedores_observacion/$', ReporteVendedoresPorObservacionListAPIView.as_view())
]


