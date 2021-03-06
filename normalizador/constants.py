# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

PROVINCIA_EXISTS=_(u"Ya existe una provincia con el nombre ingresado.")
PROVINCIA_NO_EXISTE=_("No existe la provincia ingresado.")

LOCALIDA_EXISTE=_(u"Ya existe una localidad con el nombre ingresado.")
LOCALIDAD_NO_EXISTE=_("No existe la localidad ingresado.")

CUADRANTE_EXISTE=_(u"Ya existe un cuadrante con el nombre ingresado.")
CUADRANTE_NO_EXISTE=_("No existe el cuadrante ingresado.")

BARRIO_EXISTE=_(u"Ya existe un barrio con el nombre ingresado.")
BARRIO_NO_EXISTE=_(u"No existe el barrio ingresado.")

CALLE_EXISTS=_(u"Ya existe una calle con el nombre ingresado.")
CALLE_NO_EXISTE=_("No existe la calle ingresado.")

CALLE_BARRIO_EXISTE=_(u"La calle ya se encuentra asociada al barrio.")

CAMPO_REQUERIDO=_(u"Este campo es requerido.")

OR=0
AND=1
CHOICES_OPERATOR=(
    (OR, 'OR'),
    (AND, 'AND')
)
