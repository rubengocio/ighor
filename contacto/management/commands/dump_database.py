# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        import os
        import time

        config = settings.DATABASES

        default = config['default']

        self.stdout.write(u"Buscando configuracion...")

        if default.get('HOST', None):
            self.stdout.write(u"Produccion")

            NAME = default.get('NAME')
            USER = default.get('USER')
            PASSWORD = default.get('PASSWORD')
            HOST = default.get('HOST')
            BACKUP_DIR = settings.BASE_DIR + '/backup'

            datetime = time.strftime('%m%d%Y-%H%M%S')
            datetimeBackupDir = BACKUP_DIR + datetime

            self.stdout.write(u"Creando directorio")
            if not os.path.exists(datetimeBackupDir):
                os.makedirs(datetimeBackupDir)

            mysqldump_cmd = "mysqldump -u " + USER + " --password='" + PASSWORD + "' -h " + HOST + " --databases '" + NAME + "' > " + datetimeBackupDir + "/" + NAME + ".sql"
            os.system(mysqldump_cmd)
            self.stdout.write(u"fin dump..")

        self.stdout.write(u"Listo!")