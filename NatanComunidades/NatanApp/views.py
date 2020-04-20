from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse


from django.contrib.auth.decorators import login_required # para el login
from django.contrib.auth import authenticate, login,logout

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
  if not request.user.is_authenticated: 
    return render(request,"prueba_login.html")
  #Trata de cargar de forma predeterminada 
  
  articulos = Articulo.objects.all()
  return render(request, 'index.html', {'articulos':articulos})


# Pedidos

def cargar(request):
  if not request.user.is_authenticated:
        return render(request,'prueba_login.html')
  donante = request.POST.get('donante')
  imagen = request.POST.get('imagen')
  donacion = Donacion(donante = donante, imagen = imagen)
  donacion.save()
  
  
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
  if not request.user.is_authenticated:
        return render(request,'prueba_login.html')
  global lista_articulos #usado para almacenar lo que viene por ajax
  global lista_cantidades # cuidar el uso de variables globales
  lista_articulos=[] # vaciamos por si es que viene una nueva solicitud reemplazando la anterior 
  lista_cantidades1=[]
  lista_articulos=request.POST.getlist('articulos[]')
  lista_cantidades=request.POST.getlist('cantidades[]')
  print(articulos)
  print(cantidades)

  return JsonResponse({"mensaje":"Agregado"})


def mapa(request):
  if not request.user.is_authenticated:
        return render(request,'prueba_login.html')

  datos_comunidades=consulta_datos()
  lista=[ ]
  for item in datos_comunidades:
      if item.entregado:
        entregado=1
      else:
        entregado=0
      cada_dato={"nombre":item.nombre ,"responsable": item.responsable,
                    "ubicacion": {"latitud": item.latitud,
                                    "longitud": item.longitud
                                  },
                           "entregado":entregado
                }
      lista.append(cada_dato) # agregamos a la lista

  data = {"geo": lista} # al final enviamos esto 
  return render (request,'map.html',data)
  



def solcitud_login(request):
    """
    Aca se manejan las solicitudes de login 
    
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print("el usuario es: ", user )
    if user is not None and user.is_active: 
        login(request,user)
        return HttpResponseRedirect(reverse("home"))
    return render(request,'prueba_login.html',{'mensaje':"Credenciales invalidas  "})


def logout_request(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


def consulta_datos():
  """
  Funcion que devuelve toda la info de las comundidades\n
  Devuelve en formato querydict
  """
  return Comunidad.objects.all()