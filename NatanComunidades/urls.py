"""NatanComunidades URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from NatanComunidades.NatanApp import views
from NatanComunidades.NatanApp.views import register_user
from NatanComunidades.NatanApp.views import *
from django.conf import settings # new
from django.urls import path, include # new
from django.conf.urls.static import static # new


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('cargar/', cargar),
    path('cargardb/', cargardb),
    path('cargarlista', cargar_lista_articulos),
    path('mapa/', mapa),
    path('solicitud_login',solcitud_login),
    path('logout',logout),
    path('register/', register_user, name="register"),
    # path('cargar_donacion', cargar_donacion),
    path('donaciones', ver_donaciones),
    path('mapa_cargar',mapa_cargar),
    path('comunidades',comunidades),
    path('actualizar_orden',actualizar_orden ),
    path('register',register_user),
    path('mapa_distribucion',mapa_distribucion),
    path('crear_roles',crear_roles)
]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
