# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from django.conf import settings

from contacto.models import ContactoNormalizado
from contacto.models import Titular
from celery import Celery

from normalizador.models.calle import Calle

app = Celery('contacto', broker=settings.CELERY_BROKER_URL)


logger = get_task_logger(__name__)


@app.task
def quitar_espacios():
    logger.info("quitando espacios")
    print('paso')
    Titular.quitar_espacios()
    Calle.quitar_espacios()

@app.task
def actualizar_provincia():
    ContactoNormalizado.actualizar_provincia()

@app.task
def actualizar_localidad():
    ContactoNormalizado.actualizar_localidad()