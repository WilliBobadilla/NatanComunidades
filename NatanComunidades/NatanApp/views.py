from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import logout as do_logout


from .forms import UploadImageForm


from django.contrib.auth.decorators import login_required # para el login
from django.contrib.auth import authenticate, login

from NatanComunidades.NatanApp.models import *

# Create your views here.



# ...


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
  imagen = UploadImageForm()
  articulos = Articulo.objects.all()
  return render(request, 'cargar-donacion.html', {'articulos':articulos, 'imagen': imagen})


# Pedidos

def cargar(request):
  if not request.user.is_authenticated:
        return render(request,'prueba_login.html')
  donante = request.POST.get('donante')
  donacion = Donacion()
  donacion.donante=donante
  imagen = UploadImageForm(request.POST, request.FILES)
  if imagen.is_valid():
    donacion.imagen=imagen.cleaned_data['imagen']
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
  return redirect("/")




def ver_donaciones(request):
  if not request.user.is_authenticated:
    return render(request,'prueba_login.html')
  try:
    donacionesDb = Donacion.objects.all()
  except:
    return render(request, 'ver_donaciones.html', {'msg': 'No se encontró ninguna donación.'})  
  donaciones = []
  for donacion in donacionesDb:
    donaciones.append(donacion)
    print(donaciones)
  return render(request, 'ver_donaciones.html', {'donaciones': donaciones})



@csrf_exempt 
def cargar_lista_articulos(request):
  """
  Funcion utilizada para manejar la peticion Ajax del lado del cliente\n
  Esta funcion guarda en una lista global, se actualiza con cada + que se \n
  presione o con cada borrar que se presione del lado del cliente 
  """
  if not request.user.is_authenticated:
        return render(request,'prueba_login.html')
  global lista_articulos #usado para almacenar lo que viene por ajax
  global lista_cantidades # cuidar el uso de variables globales
  lista_articulos=[] # vaciamos por si es que viene una nueva solicitud reemplazando la anterior 
  lista_cantidades1=[]
  
  lista_articulos=request.POST.getlist('articulos[]')
  lista_cantidades=request.POST.getlist('cantidades[]')
  print("listas",lista_articulos)
  print("listacant",lista_cantidades)
  return JsonResponse({"mensaje":"Agregado"})


def mapa(request):
  if request.user.is_staff:
    print("soy staff y que ")
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')
  lista=consulta_datos()
  cant_comunidades=len(Comunidad.objects.all())
  data = {"geo": lista,"cantidad_comunidades":cant_comunidades} # al final enviamos esto 
  return render (request,'map.html',data)


def mapa_cargar(request):
  """
  vista que se maneja para cargar datos de las \n
  comunidades a traves de un mapa
  """
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')
  if request.method == 'POST':
    nombre= request.POST.get("nombre")
    responsable=request.POST.get("responsable")
    latitud=float(request.POST.get("latitud"))
    longitud=float(request.POST.get("longitud"))
    meta=int(request.POST.get("meta"))
    disp=int(request.POST.get("disp"))
    entregado=request.POST.get("entregado")
    if entregado=="True":
      entregado=True
    else: 
      entregado=False 
    
    listo=request.POST.get("listo")
    if listo=="True":
      listo=True
    else: 
      listo=False 
    
    datos_comunidades=Comunidad(nombre=nombre,responsable=responsable,latitud=latitud,longitud=longitud,meta=meta,disp=disp,entregado=entregado,listo=listo)
    datos_comunidades.save()
    lista=consulta_datos()
    cant_comunidades=len(Comunidad.objects.all())
    data = {"geo": lista,"cantidad_comunidades":cant_comunidades} # al final enviamos esto 
    return render(request,'mapa_agregar_data.html',data)
  else:
    lista=consulta_datos()
    cant_comunidades=len(Comunidad.objects.all())
    data = {"geo": lista,"cantidad_comunidades":cant_comunidades} # al final enviamos esto 
    return render(request,'mapa_agregar_data.html',data)


def register_user(request):

    msg     = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg     = 'Usuario creado. Inicie sesión con sus datos.'
            success = True   
            #return redirect("/login/")
        else:
            msg = 'El formulario no es válido, intente nuevamente.'    
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form, "msg" : msg, "success" : success })




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

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')
    
def logout_request(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

def consulta_datos():
  """
  Funcion que devuelve toda la info de las comundidades\n
  Devuelve en formato diccionario
  """
  datos_comunidades=Comunidad.objects.all()
  lista=[ ]
  for item in datos_comunidades:
      if item.entregado:
        entregado=1
      else:
        entregado=0
      cada_dato={"nombre":item.nombre ,"responsable": item.responsable,"meta":item.meta,
                    "ubicacion": {"latitud": item.latitud,
                                    "longitud": item.longitud
                                  },
                           "entregado":entregado
                }
      lista.append(cada_dato) # agregamos a la lista
  return lista 