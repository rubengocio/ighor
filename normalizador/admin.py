from django.contrib import admin

from normalizador.models import Criterio
from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)

class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia', 'estado')
    list_filter = ('provincia', 'estado')


class CuadranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad', 'estado')
    list_filter = ('estado',)

class BarrioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuadrante', 'estado')
    list_filter = ('cuadrante', 'estado')

class CalleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)

class CallesBarrioAdmin(admin.ModelAdmin):
    list_display = ('calle', 'altura_desde', 'altura_hasta', 'barrio', 'cuadrante', 'localidad', 'provincia')

    def cuadrante(self, obj):
        return obj.barrio.cuadrante.nombre

    def localidad(self, obj):
        return obj.barrio.cuadrante.localidad.nombre

    def provincia(self, obj):
        return obj.barrio.cuadrante.localidad.provincia.nombre

admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Cuadrante, CuadranteAdmin)
admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Calle, CalleAdmin)
admin.site.register(CallesBarrio, CallesBarrioAdmin)
admin.site.register(Criterio)
