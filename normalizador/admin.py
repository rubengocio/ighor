from django.contrib import admin
from django.db import IntegrityError
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from normalizador.models import Criterio
from normalizador.models import DiccionarioBarrio
from normalizador.models import DiccionarioCalle
from normalizador.models.barrio import Barrio
from normalizador.models.calle import Calle
from normalizador.models.calles_barrio import CallesBarrio
from normalizador.models.cuadrante import Cuadrante
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia
from import_export.fields import Field


class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', )


class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'provincia', 'estado')
    list_filter = ('provincia', 'estado')
    search_fields = ('nombre', 'provincia__nombre')


class CuadranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'localidad', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', 'localidad__nombre')


class BarrioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cuadrante', 'estado')
    list_filter = ('cuadrante', 'estado')
    search_fields = ('nombre', 'cuadrante__nombre')


class CalleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre',)


class CallesBarrioResource(resources.ModelResource):
    barrio = Field(attribute='barrio', column_name='BARRIO')
    calle = Field(attribute='calle', column_name='CALLE')
    altura_desde = Field(attribute='altura_desde', column_name='ALTURA_DESDE')
    altura_hasta = Field(attribute='altura_hasta', column_name='ALTURA_HASTA')
    referencia = Field(attribute='referencia', column_name='REFERENCIA')
    plano = Field(attribute='plano', column_name='PLANO')
    ubicacion = Field(attribute='ubicacion', column_name='UBICACION')
    tipo_numeracion = Field(attribute='tipo_numeracion', column_name='TIPO_NUMERACION')
    nomenclado = Field(attribute='nomenclado', column_name='NOMENCLADO')

    class Meta:
        model = CallesBarrio
        exclude = ('id',)
        import_id_fields = ('barrio', 'calle')

    def before_import_row(self, row, **kwargs):
        name = self.__class__
        try:
            try:
                barrio = row['BARRIO']
                calle = row['CALLE']
                tipo_numeracion = row['TIPO_NUMERACION']
                nomenclado = row['NOMENCLADO'].strip()

                nomenclado = '1' if nomenclado == 'True' else '0'

                barrio = Barrio.objects.filter(id=barrio).first()
                calle = Calle.objects.filter(id=calle).first()

                try:
                    tipo_numeracion = int(tipo_numeracion)
                except Exception:
                    tipo_numeracion = CallesBarrio.ALL

                if tipo_numeracion == CallesBarrio.PAIR:
                    tipo_numeracion = CallesBarrio.PAIR
                elif tipo_numeracion == CallesBarrio.ODD:
                    tipo_numeracion = CallesBarrio.ODD
                else:
                    tipo_numeracion = CallesBarrio.ALL

                if int(nomenclado) == 1:
                    nomenclado = True
                else:
                    nomenclado = False

                row['BARRIO'] = barrio
                row['CALLE'] = calle
                row['TIPO_NUMERACION'] = tipo_numeracion
                row['NOMENCLADO'] = nomenclado

            except Exception as ex:
                row['BARRIO'] = None
                row['CALLE'] = None
                row['TIPO_NUMERACION'] = None
                row['NOMENCLADO'] = None

            super(name, self).before_import_row(row, **kwargs)
        except IntegrityError:
            pass


class CallesBarrioAdmin(ImportExportModelAdmin):
    resource_class = CallesBarrioResource
    list_display = ('calle', 'altura_desde', 'altura_hasta', 'barrio', 'cuadrante', 'localidad', 'provincia')
    search_fields = ('calle', 'barrio__nombre')

    def cuadrante(self, obj):
        return obj.barrio.cuadrante.nombre

    def localidad(self, obj):
        return obj.barrio.cuadrante.localidad.nombre

    def provincia(self, obj):
        return obj.barrio.cuadrante.localidad.provincia.nombre


class DiccionarioBarrioAdmin(admin.ModelAdmin):
    list_display = ('barrio', 'nombre')
    search_fields = ('barrio__nombre', 'nombre')


class DiccionarioCalleAdmin(admin.ModelAdmin):
    list_display = ('calle_barrio', 'calle_incorrecta')
    search_fields = ('calle_barrio', 'calle_incorrecta')


admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(Cuadrante, CuadranteAdmin)
admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Calle, CalleAdmin)
admin.site.register(CallesBarrio, CallesBarrioAdmin)
admin.site.register(Criterio)
admin.site.register(DiccionarioBarrio, DiccionarioBarrioAdmin)
admin.site.register(DiccionarioCalle, DiccionarioCalleAdmin)
