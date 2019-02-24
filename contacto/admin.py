from django.contrib import admin

# Register your models here.
from django.db import IntegrityError
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from contacto import commons
from contacto.models import ContactoNormalizado
from contacto.models.cliente_jk import ClienteJK
from contacto.models.titular import Titular
from import_export.signals import post_import
from django.dispatch import receiver

from contacto.tasks import quitar_espacios, actualizar_provincia, actualizar_localidad, actualizar_barrio, \
    actualizar_calle, actualizar_normalizados
from normalizador.tasks import actualizar_diccionario_barrio, actualizar_contacto


class ClienteJKResource(resources.ModelResource):
    cod_cliente = Field(attribute='cod_cliente', column_name='COD_CLIENTE')
    nombre = Field(attribute='nombre', column_name='NOMBRE')
    tipo_documento = Field(attribute='tipo_documento', column_name='TIPO_DOCUMENTO')
    nro_documento = Field(attribute='nro_documento', column_name='NRO_DOCUMENTO')
    telefono = Field(attribute='telefono', column_name='TELEFONO')
    calle = Field(attribute='calle', column_name='CALLE')
    numero = Field(attribute='numero', column_name='NRO')
    barrio = Field(attribute='barrio', column_name='BARRIO')
    codigo_postal = Field(attribute='codigo_postal', column_name='CODIGO_POSTAL')
    cuadrante = Field(attribute='cuadrante', column_name='CUADRANTE')
    cualidad = Field(attribute='cualidad', column_name='Cualidad')
    inhumados = Field(attribute='inhumados', column_name='Inhumados')
    productos = Field(attribute='productos', column_name='Productos')
    meses_deuda = Field(attribute='meses_deuda', column_name='MesesDeuda')
    monto_deuda = Field(attribute='monto_deuda', column_name='MontoDeuda')
    tel_naranja = Field(attribute='tel_naranja', column_name='TelNaranja')
    tel_jakemate_1 = Field(attribute='tel_jakemate_1', column_name='TelJakeMate1')
    tel_jakemate_2 = Field(attribute='tel_jakemate_2', column_name='TelJakeMate2')
    tel_jakemate_3 = Field(attribute='tel_jakemate_3', column_name='TelJakeMate3')
    ultimo_pago = Field(attribute='ultimo_pago', column_name='UltimoPago')

    class Meta:
        model = ClienteJK
        exclude = ('id',)
        import_id_fields = ('tipo_documento','nro_documento')

    def before_import_row(self, row, **kwargs):
        name = self.__class__
        try:
            try:
                row['TIPO_DOCUMENTO'] = commons.get_tipo_documento(row['TIPO_DOCUMENTO'])
            except Exception as ex:
                row['TIPO_DOCUMENTO'] = 0

            super(name, self).before_import_row(row, **kwargs)
        except IntegrityError:
            pass


class ClienteJKAdmin(ImportExportModelAdmin):
    resource_class = ClienteJKResource
    list_display = ('nombre', 'tipo_documento', 'nro_documento')
    search_fields = ('nombre', 'nro_documento')


class TitularResource(resources.ModelResource):
    estado = Field(attribute='estado', column_name='EstadoListin')
    tipo = Field(attribute='tipo', column_name='Tipo')
    descripcion = Field(attribute='descripcion', column_name='Descr')
    titular = Field(attribute='titular', column_name='Titular')
    apellido = Field(attribute='apellido', column_name='Apellido')
    nombre = Field(attribute='nombre', column_name='Nombre')
    domicilio_calle = Field(attribute='domicilio_calle', column_name='DomParticularCalle')
    domicilio_numero = Field(attribute='domicilio_numero', column_name='Nro')
    domicilio_piso = Field(attribute='domicilio_piso', column_name='Piso')
    domicilio_depto = Field(attribute='domicilio_depto', column_name='Dpto')
    domicilio_barrio = Field(attribute='domicilio_barrio', column_name='Barrio')
    telefono = Field(attribute='telefono', column_name='Telefono')
    codigo_postal = Field(attribute='codigo_postal', column_name='CodPos')
    localidad = Field(attribute='localidad', column_name='Localidad')
    lp = Field(attribute='lp', column_name='LP')
    provincia = Field(attribute='provincia', column_name='Provincia')
    empresas = Field(attribute='empresas', column_name='Empresas')
    domicilio_laboral_calle = Field(attribute='domicilio_laboral_calle', column_name='DomLaboralCalle')
    domicilio_laboral_numero = Field(attribute='domicilio_laboral_numero', column_name='DomLaboralNro')
    domicilio_laboral_piso = Field(attribute='domicilio_laboral_piso', column_name='DomLaboralPiso')
    domicilio_laboral_depto = Field(attribute='domicilio_laboral_depto', column_name='DomLaboralDpto')
    domicilio_laboral_barrio = Field(attribute='domicilio_laboral_barrio', column_name='DomLaboralBarrio')
    domicilio_laboral_telefono = Field(attribute='domicilio_laboral_telefono', column_name='DomLaboralTelefono')
    domicilio_laboral_codigo_postal = Field(attribute='domicilio_laboral_codigo_postal', column_name='DomLaboralCodPos')
    domicilio_laboral_localidad = Field(attribute='domicilio_laboral_localidad', column_name='DomLaboralLocalidad')
    domicilio_laboral_lp = Field(attribute='domicilio_laboral_lp', column_name='DomLaboralLP')
    domicilio_laboral_provincia = Field(attribute='domicilio_laboral_provincia', column_name='DomLaboralProvincia')
    telefono_alternativo = Field(attribute='telefono_alternativo', column_name='TelAlternativo')
    sexo = Field(attribute='sexo', column_name='Sexo')
    fecha_nacimiento = Field(attribute='fecha_nacimiento', column_name='FecNac')
    fecha_alta = Field(attribute='fecha_alta', column_name='FecAlta')
    tipo_cuenta = Field(attribute='tipo_cuenta', column_name='TipoCuenta')

    class Meta:
        model = Titular
        exclude = ('id',)
        import_id_fields = ('tipo', 'titular')

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        name = self.__class__
        try:
            try:
                instance.fecha_alta = str(int(instance.fecha_alta.replace('/', '')))
            except Exception as ex:
                instance.fecha_alta = 0

            try:
                instance.fecha_nacimiento = str(int(instance.fecha_nacimiento.replace('/', '')))
            except Exception as ex:
                instance.fecha_nacimiento = 0

            super(name, self).save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass


class TitularAdmin(ImportExportModelAdmin):
    resource_class = TitularResource
    list_display = ('titular','descripcion','apellido','nombre')
    search_fields = ('titular', 'apellido', 'nombre')

    def save_form(self, request, form, change):

        obj = super(TitularAdmin, self).save_form(request, form, change)
        if obj.has_normalized():
            obj.normalizar_contacto()
            ejecutar_procesos()

        return obj


class IsBarrioNormalizadoFilter(admin.SimpleListFilter):
    title = 'Barrio Normalizado'
    parameter_name = '_barrio'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(barrio__isnull=False)
        elif value == 'No':
            return queryset.filter(barrio__isnull=True)
        return queryset


class IsCalleNormalizadoFilter(admin.SimpleListFilter):
    title = 'Calle Normalizada'
    parameter_name = '_calle'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(calle__isnull=False)
        elif value == 'No':
            return queryset.filter(calle__isnull=True)
        return queryset


class ContactoNormalizadoAdmin(admin.ModelAdmin):
    list_display = ('titular', 'apellido', 'nombre', 'estado', '_provincia', '_localidad', '_barrio', '_calle', 'fecha_actualizacion')
    raw_id_fields = ('calle', 'barrio', 'provincia', 'localidad')
    list_filter = (IsBarrioNormalizadoFilter, IsCalleNormalizadoFilter)
    search_fields = ('titular','apellido', 'nombre')

    def _provincia(self, obj):
        return True if obj.provincia else False

    def _localidad(self, obj):
        return True if obj.localidad else False

    def _barrio(self, obj):
        return True if obj.barrio else False

    def _calle(self, obj):
        return True if obj.calle else False

    _provincia.boolean = True
    _localidad.boolean = True
    _barrio.boolean = True
    _calle.boolean = True


admin.site.register(Titular, TitularAdmin)
admin.site.register(ClienteJK, ClienteJKAdmin)
admin.site.register(ContactoNormalizado, ContactoNormalizadoAdmin)

def ejecutar_procesos():
    # quito los espacios en blanco
    quitar_espacios()
    # insert los nuevos contactos
    actualizar_contacto()
    # actualizo la provincia de los contactos
    actualizar_provincia()
    # actualizo la localidad de los contactos
    actualizar_localidad()
    # actualizo los barrios de los contactos
    actualizar_barrio()
    # actualizo las calles de los contactos
    actualizar_calle()
    # actualizo el diccionario de barrios
    actualizar_diccionario_barrio()
    # actualizo los contactos que se han normalizado
    actualizar_normalizados()


@receiver(post_import, dispatch_uid='_post_import')
def _post_import(model, **kwargs):
    # Solo ejecuto los procesos si se importa el modelo Titular
    if model.__name__ == Titular.__name__:
        ejecutar_procesos()