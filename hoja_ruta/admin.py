from django.contrib import admin

# Register your models here.
from contacto.models import ContactoNormalizado
from hoja_ruta.models import HojaRuta, DetalleHojaRuta


class DetalleHojaRutaInline(admin.TabularInline):
    contact=None
    model = DetalleHojaRuta
    readonly_fields = (
        'numero_orden',
        'tipo',
        'titular',
        'apellido',
        'nombre',
        'provincia',
        'localidad',
        'barrio',
        'calle',
        'altura',
        'piso',
        'departamento',
        'observaciones'
    )
    exclude = ('id',)

    def apellido(self, obj):
        contact=ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.apellido

    def nombre(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.nombre

    def provincia(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.provincia

    def localidad(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.localidad

    def barrio(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.barrio

    def calle(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.calle

    def altura(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.altura

    def piso(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.piso

    def departamento(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.departamento

    def observaciones(self, obj):
        contact = ContactoNormalizado.objects.filter(tipo=obj.tipo, titular=obj.titular).first()
        return contact.observaciones


class HojaRutaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'calle_barrio')
    inlines=[DetalleHojaRutaInline,]
    readonly_fields = (
        'numero',
        'calle_barrio',
        'altura_desde',
        'altura_hasta'
    )

    def altura_desde(self, obj):
        return obj.calle_barrio.altura_desde

    def altura_hasta(self, obj):
        return obj.calle_barrio.altura_hasta


admin.site.register(HojaRuta, HojaRutaAdmin)