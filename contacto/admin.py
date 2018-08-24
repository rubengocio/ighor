from django.contrib import admin

# Register your models here.
from django.dispatch import receiver
from import_export import resources
from import_export import widgets
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.signals import post_import

from contacto.models.titular import Titular
from normalizador.models import DiccionarioBarrio


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
        import_id_fields = ('tipo','titular')


class TitularAdmin(ImportExportModelAdmin):
    resource_class = TitularResource
    list_display = ('titular','descripcion','apellido','nombre')


admin.site.register(Titular, TitularAdmin)

@receiver(post_import, dispatch_uid='_post_import')
def _post_import(model, **kwargs):
    # model is the actual model instance which after import
    DiccionarioBarrio.actualizar_diccionario_barrio()