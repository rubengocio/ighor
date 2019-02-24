# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from django.conf import settings

from contacto.models import ContactoNormalizado
from normalizador.models import CalleIncorrecta
from normalizador.models import DiccionarioBarrio

from celery import Celery

from normalizador.models.calle import Calle

app = Celery('normalizador', broker=settings.CELERY_BROKER_URL)

logger = get_task_logger(__name__)


@app.task
def actualizar_diccionario_barrio():
    logger.info("diccionario barrio")
    print('actualizando diccionario de barrios')
    DiccionarioBarrio.actualizar_diccionario_barrio()

@app.task
def actualizar_contacto():
    logger.info("actualizar contacto")
    print('actualizando contactos')
    ContactoNormalizado.actualizar_contacto()

@app.task
def actualizar_calle_incorrecta(barrio_id):
    CalleIncorrecta.actualizar_calle_incorrecta(barrio_id)
