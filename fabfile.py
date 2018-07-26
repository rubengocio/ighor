from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.colors import red, green
from fabric.contrib.project import rsync_project
from fabric.operations import get, put
#from cuisine import *
from django.conf import settings
import sys
import psycopg2

# !/bin/bash
# query importante para dar permisos al usuario que se encarga de los reportes
# "grant select on ALL TABLES in schema public TO reporting;"

env.dbname = settings.DATABASES['default']['NAME']
env.dbuser = settings.DATABASES['default']['USER']
env.dbpassword = settings.DATABASES['default']['PASSWORD']


def virtualenv(command):
    """
    Run a command in the virtualenv. This prefixes the command with the source
    command.
    Usage:
        virtualenv('pip install django')
    """
    source = 'source {virt_dir}/bin/activate && '.format(virt_dir=env.project_base + "/venv")
    run(source + command)


def develop():
    env.hosts = ['169.57.130.245']
    # env.key_filename = '~/key/rsa_server.priv.key'
    env.user = 'adm1'
    # env.password = 'ilikemd2014'
    # env.report_user = 'reporting'
    # env.report_password = 'mobyreporting'
    env.project_base = '/home/rgocio/ighor/ighor'
    env.project_name = 'ighor'
    env.settings = 'ighor.settings.py'
    env.project_repo = 'https://github.com/rubengocio/ighor.git'

    env.domain = 'rgocio.pythonanywhere.com'
    env.username = 'rgocio'
    env.token = '09d89a5b0a0889e26d1c755b3dac45bb64f3609b'

    #env.process = 'mercosur_py'


def update_changes():
    logs_dir = env.project_base + 'logs'
    run_dir = env.project_base + 'run'
    virt_dir = env.project_base + 'venv'
    static_dir = env.project_base + 'src/static'
    media_dir = env.project_base + 'src/media'
    #dir_ensure(logs_dir, owner=env.user, group=env.user)
    #dir_ensure(run_dir, owner=env.user, group=env.user)
    #dir_ensure(static_dir, owner=env.user, group=env.user)
    #dir_ensure(media_dir, owner=env.user, group=env.user)

    puts(green('Updating changes from repo'))
    with cd(env.project_base + 'src'):
        run('git checkout -- .')
        run('git pull')

        puts(green('Update virtualenv project dependencies'))
        virtualenv('pip install -r requirements.txt')

        puts(green('Database migrations and syncdb'))
        #virtualenv('python manage.py syncdb --settings={settings}'.format(
        #    settings=env.settings,
        #))
        virtualenv('python manage.py migrate --settings={settings}'.format(
            settings=env.settings,
        ))


        virtualenv('python manage.py collectstatic --noinput -l -i media')
        puts(green('Finished OK'))
        restart_app_server()


def restart_app_server():
    run("echo 'flush_all' | netcat localhost 11211")
    puts(green('Reloading the supervisor process'))
    run('supervisorctl restart {process}'.format(process=env.process))






