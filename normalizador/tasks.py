# -*- coding: utf-8 -*-
from celery.utils.log import get_task_logger
from django.conf import settings

from contacto.models import ContactoNormalizado
from normalizador.models import CalleIncorrecta
from normalizador.models import DiccionarioBarrio

from celery import Celery

app = Celery('normalizador', broker=settings.CELERY_BROKER_URL)

logger = get_task_logger(__name__)


@app.task
def actualizar_diccionario_barrio():
    logger.info("diccionario barrio")
    DiccionarioBarrio.actualizar_diccionario_barrio()

@app.task
def actualizar_contacto():
    logger.info("actualizar contacto")
    ContactoNormalizado.actualizar_contacto()

@app.task
def actualizar_calle_incorrecta(barrio_id):
    CalleIncorrecta.actualizar_calle_incorrecta(barrio_id)