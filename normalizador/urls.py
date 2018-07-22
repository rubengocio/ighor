# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework import routers

from normalizador.views.barrio import BarrioViewSet
from normalizador.views.cuadrante import CuadranteViewSet, CuadranteBarriosRetrieveAPIView
from normalizador.views.localidad import LocalidadViewSet, LocalidadCuadrantesRetrieveAPIView
from normalizador.views.provincia import ProvinciaViewSet, ProvinciaLocalidadesRetrieveAPIView

router = routers.SimpleRouter()

router.register(r'provincia', ProvinciaViewSet)
router.register(r'localidad', LocalidadViewSet)
router.register(r'cuadrante', CuadranteViewSet)
router.register(r'barrio', BarrioViewSet)

urlpatterns = router.urls


urlpatterns += [
    path(r'provincia/<int:pk>/localidades/', ProvinciaLocalidadesRetrieveAPIView.as_view()),
    path(r'localidad/<int:pk>/cuadrantes/', LocalidadCuadrantesRetrieveAPIView.as_view()),
    path(r'cuadrante/<int:pk>/barrios/', CuadranteBarriosRetrieveAPIView.as_view())
]


