from django.contrib import admin

# Register your models here.
from normalizador.models.barrio import Barrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia


class ProvinciaAdmin(admin.ModelAdmin):
    pass


class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia')
    list_filter = ('provincia',)


class CuadranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad')


class BarrioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuadrante')
    list_filter = ('cuadrante',)


admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Cuadrante, CuadranteAdmin)
admin.site.register(Barrio, BarrioAdmin)