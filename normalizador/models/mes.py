# -*- coding: utf-8 -*-
from django.db import models


class Mes(models.Model):
    codigo = models.IntegerField()
    nombre = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return u'%s' % self.nombre

    def __unicode__(self):
        return u'%s' % self.nombre