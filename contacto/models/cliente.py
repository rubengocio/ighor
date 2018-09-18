# -*- coding: utf-8 -*-
from django.db import models

class Cliente(models.Model):
    codigo_cliente=models.IntegerField(unique=True)
    nombre_completo=models.CharField(max_length=200)
    apellido=models.CharField(max_length=100)
    nombre=models.CharField(max_length=100)
    tipo_documento=models.CharField(max_length=6)
    numero_documento=models.IntegerField(db_index=True)
    telefono=models.CharField(max_length=50)
    calle=models.CharField(max_length=50)
    altura=models.CharField(max_length=10)
    barrio=models.CharField(max_length=50)
    codigo_postal=models.IntegerField()
    parcela=models.CharField(max_length=10)
    ss=models.CharField(max_length=10)
    ss = models.CharField(max_length=10)
    ss_gs = models.CharField(max_length=10)
    emi = models.CharField(max_length=10)
    cualidad=models.IntegerField()
    inhumados=models.CharField(max_length=4)
    parcela_inhumados=models.IntegerField()
    meses_deuda=models.IntegerField()
    monto_deuda=models.DecimalField(decimal_places=2,max_digits=20)
    productos=models.CharField(max_length=100)

    def __str__(self):
        return u'%s' % self.codigo_cliente

    def __unicode__(self):
        return u'%s' % self.codigo_cliente