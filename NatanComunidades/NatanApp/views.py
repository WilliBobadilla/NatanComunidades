from django.shortcuts import render
from NatanComunidades.NatanApp.models import *

# Create your views here.

## Vistas

def home(request):
  articulos = Articulo.objects.all()
  print(request) 
  return render(request, 'index.html', {'articulos':articulos})


# Pedidos

def cargar(request):
  donante = request.POST.get('donante')
  imagen = request.POST.get('imagen')
  donacion = Donacion(donante = donante, imagen = imagen)
  donacion.save()
  articuloID = request.POST.get('articulo')
  articulo = Articulo.objects.get(id=articuloID)
  cantidad = request.POST.get('cantidad')
  donacionxarticulo = Donacionxarticulo(donacion=donacion, articulo=articulo, cantidad=cantidad)
  donacionxarticulo.save()
  return home(request)