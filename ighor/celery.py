# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from celery import Celery

# for django projects
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ighor.settings.base')
app = Celery('ighor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
