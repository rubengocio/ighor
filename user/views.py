# -*- encoding: utf-8 -*-

# Create your views here.
VENTAS=u'Ventas'
GERENCIA=u'Gerencia'
ADMINISTRADOR=u'Administrador'


def jwt_response_payload_handler(token, user=None, request=None):
    """

    :param token:
    :param user:
    :param request:
    :return:
    """
    rol={
        'iso': 'ADM',
        'name': ADMINISTRADOR
    }

    if user.groups.filter(name='VENTAS').first():
        rol={
            'id': 'VEN',
            'name': ADMINISTRADOR
        }
    elif user.groups.filter(name='GERENCIA').first():
        rol = {
            'id': 'GER',
            'name': GERENCIA
        }

    payload = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'rol': rol,
        'token': token,
    }

    return payload