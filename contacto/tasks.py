# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from django.conf import settings

from contacto.models import ContactoNormalizado
from contacto.models import Titular
from celery import Celery

from normalizador.models.calle import Calle
from normalizador.models.localidad import Localidad
from normalizador.models.provincia import Provincia

app = Celery('contacto', broker=settings.CELERY_BROKER_URL)


logger = get_task_logger(__name__)


@app.task
def quitar_espacios():
    logger.info("quitando espacios")
    print('quitando espacios en provincias')
    Provincia.quitar_espacios()
    print('quitando espacios en localidades')
    Localidad.quitar_espacios()
    print('quitando espacios en calles')
    Calle.quitar_espacios()
    print('quitando espacios en titulares')
    Titular.quitar_espacios()


@app.task
def actualizar_provincia():
    print('actualizando provincia')
    ContactoNormalizado.actualizar_provincia()

@app.task
def actualizar_localidad():
    print('actualizando localidades')
    ContactoNormalizado.actualizar_localidad()

@app.task
def actualizar_barrio():
    print('actualizando barrios')
    ContactoNormalizado.actualizar_barrios()

@app.task
def actualizar_calle():
    print('actualizando calles')
    ContactoNormalizado.actualizar_calles()

@app.task
def actualizar_normalizados():
    print('actualizando normalizados')
    ContactoNormalizado.actualizar_normalizados()