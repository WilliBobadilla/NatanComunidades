from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from NatanComunidades.NatanApp.models import *

# Create your views here.

lista_articulos=[]
lista_cantidades=[]
#Función para cargar los datos predeterminados
def cargardb(request):
  try:
    medidas = ('Kg', 'L', 'unidad')
    instancias = []

    for medida in medidas:
      instancias.append(Medida(simbolo=medida))
    
    Medida.objects.bulk_create(instancias)
  except:
    pass
  try:
    articulos = (
      ('Azúcar',Medida.objects.get(simbolo ='Kg')),
      ('Leche en polvo/cartón', Medida.objects.get(simbolo ='L')),
      ('Yerba', Medida.objects.get(simbolo ='Kg')),
      ('Panificados secos', Medida.objects.get(simbolo ='Kg')),
      ('Harina', Medida.objects.get(simbolo ='Kg')),
      ('Aceite', Medida.objects.get(simbolo ='L')),
      ('Pollo/Carne enlatada', Medida.objects.get(simbolo ='unidad')),
      ('Poroto', Medida.objects.get(simbolo ='Kg')),
      ('Arroz', Medida.objects.get(simbolo ='Kg')),
      ('Fideo', Medida.objects.get(simbolo ='Kg')),
      ('Detergente', Medida.objects.get(simbolo ='L')),
      ('Jabón en pan', Medida.objects.get(simbolo ='unidad')),
      ('Alcohol líquido a 70%', Medida.objects.get(simbolo ='L')),
      ('Sal', Medida.objects.get(simbolo ='Kg')),
      ('Lavandina', Medida.objects.get(simbolo ='L')),
      )
    instancias = []

    for articulo in articulos:
      instancias.append(Articulo(nombre=articulo[0], medida=articulo[1]))

    Articulo.objects.bulk_create(instancias)
  except:
    pass

  return home(request)

## Vistas

def home(request):
  #Trata de cargar de forma predeterminada 
  articulos = Articulo.objects.all()
  return render(request, 'index.html', {'articulos':articulos})


# Pedidos

def cargar(request):
  donante = request.POST.get('donante')
  imagen = request.POST.get('imagen')
  donacion = Donacion(donante = donante, imagen = imagen)
  donacion.save()
<<<<<<< Updated upstream
  
  
  global lista_articulos #usado para almacenar lo que viene por ajax
  global lista_cantidades # cuidar el uso de variables globales
  # vemos la donacion por articulo
  for item in range(len(lista_articulos)):
    articuloID = lista_articulos[item] 
    articulo = Articulo.objects.get(id=articuloID)
    cantidad= lista_cantidades[item]
    donacionxarticulo = Donacionxarticulo(donacion=donacion, articulo=articulo, cantidad=cantidad)
    donacionxarticulo.save()
  #vaciamos la varible global antes de cargar otro donante
  lista_articulos=[]
  lista_articulos=[]
  return home(request)


@csrf_exempt 
def cargar_lista_articulos(request):
  """
  Funcion utilizada para manejar la peticion Ajax del lado del cliente\n
  Esta funcion guarda en una lista global
  """
  global lista_articulos #usado para almacenar lo que viene por ajax
  global lista_cantidades # cuidar el uso de variables globales

  lista_articulos=request.POST.getlist('articulos[]')
  lista_cantidades=request.POST.getlist('cantidades[]')
  print(articulos)
  print(cantidades)

  return JsonResponse({"mensaje":"Agregado"})

  
=======
  articuloID = request.POST.get('articulo')
  articulo = Articulo.objects.get(id=articuloID)
  cantidad = request.POST.get('cantidad')
  donacionxarticulo = Donacionxarticulo(donacion=donacion, articulo=articulo, cantidad=cantidad)
  donacionxarticulo.save()
  return home(request)

def mapa(request):
  return render (request,'map.html')
  
>>>>>>> Stashed changes
