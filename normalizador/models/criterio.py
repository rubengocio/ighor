# -*- coding: utf-8 -*-
from django.db import models


class Criterio(models.Model):
    nombre=models.CharField(max_length=127)
    valor=models.CharField(max_length=127)

    def __str__(self):
        return u'%s' % self.nombre

    def __unicode__(self):
        return u'%s' % self.nombre