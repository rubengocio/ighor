# -*- coding: utf-8 -*-

DNI = 1
LE = 2
LC = 3
NN = 5

TIPO_DOCUMENTO_CHOICES = (
    (DNI, 'DNI'),
    (LE, 'LE'),
    (LC, 'LC'),
    (NN, 'NN')
)


def get_tipo_documento(value):

    if value == 'DNI':
        return DNI
    elif value == 'LE':
        return LE
    elif value == 'LC':
        return LC
    else:
        return NN

