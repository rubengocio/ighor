# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers

from user import constants


class UserSerializer(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=(
            'id',
            'first_name',
            'last_name',
            'email',
            'rol'
        )

    def get_rol(self, obj):
        rol = {
            'iso': 'ADM',
            'name': constants.ADMINISTRADOR
        }

        if obj.groups.filter(name=constants.GROUP_VENTAS).first():
            rol = {
                'id': 'VEN',
                'name': constants.ADMINISTRADOR
            }
        elif obj.groups.filter(name=constants.GROUP_GERENCIA).first():
            rol = {
                'id': 'GER',
                'name': constants.GERENCIA
            }
        elif obj.groups.filter(name=constants.GROUP_VENDEDOR).first():
            rol = {
                'id': 'UVE',
                'name': constants.VENDEDOR
            }

        return rol