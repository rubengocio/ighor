from ighor.settings.base import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rgocio$default',
        'USER': 'rgocio',
        'PASSWORD': 'ighor123',
        'HOST': 'rgocio.mysql.pythonanywhere-services.com',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}