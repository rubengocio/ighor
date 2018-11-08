# -*- encoding: utf-8 -*-

# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions

from user import constants
from user.serializers import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    """

    :param token:
    :param user:
    :param request:
    :return:
    """

    payload = UserSerializer(user).data
    payload['token'] = token

    return payload


class VendedorListAPIView(generics.ListAPIView):
    """
    Listado de vendedores
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(
        groups__name=constants.GROUP_VENDEDOR,
        is_active=True
    )
    serializer_class = UserSerializer


class VendedorRetrieveAPIView(generics.RetrieveAPIView):
    """
    Devuelve los datos del vendedor con el id ingresado
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.filter(
        groups__name=constants.GROUP_VENDEDOR,
        is_active=True
    )
    serializer_class = UserSerializer