from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Medida)
admin.site.register(Articulo)
admin.site.register(Donacion)
admin.site.register(Donacionxarticulo)
admin.site.register(Comunidad)