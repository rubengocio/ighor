"""ighor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_swagger_view(title='Ighor API')

urlpatterns = [
    url(r'^v1/', include('normalizador.urls')),
    url(r'^$', schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^v1/auth/', obtain_jwt_token),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)