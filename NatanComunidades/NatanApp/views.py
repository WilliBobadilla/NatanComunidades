from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import SignUpForm
from django.contrib.auth import logout as do_logout
from django.db.models import Sum


from .forms import UploadImageForm


from django.contrib.auth.decorators import login_required # para el login
from django.contrib.auth import authenticate, login

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
  imagen = UploadImageForm()
  articulos = Articulo.objects.all()
  return render(request, 'cargar-donacion.html', {'articulos':articulos, 'imagen': imagen})


#todos los usuarios pueden acceder a esta lista 
def ver_donaciones(request):
  if not request.user.is_authenticated:
    return render(request,'prueba_login.html')
  try:
    donaciones = Donacionxarticulo.objects.all()
    articulos = Articulo.objects.all()
  except:
    return render(request, 'ver_donaciones.html', {'msg': 'No se encontró ninguna donación.'})

  # sendArticulos = []
  # sendCantidades = []
  resultado = {}
  for articulo in articulos:
    sumatoria = donaciones.filter(articulo__nombre=articulo.nombre).aggregate(Sum('cantidad'))['cantidad__sum']
    if sumatoria:
      # sendCantidades.append(sumatoria)
      # sendArticulos.append(articulo.nombre)
      resultado[articulo.nombre] = sumatoria
      # print(sendArticulos)
      # print(sendCantidades)
  # iterable = range(len(sendArticulos)-1)
  # resultado = [sendArticulos, sendCantidades]
  print(resultado)

  return render(request, 'ver_donaciones.html', {'resultado': resultado})






## -------------------------- RECEPCION-------------------------------------------------

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
  return redirect('/')

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




# ----------------------------ADMINISTRACION------------------------------------------
# este solo pueden ver los Administradores
def mapa(request):
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')
  lista=consulta_datos()
  cant_comunidades=len(Comunidad.objects.all())
  data = {"geo": lista,"cantidad_comunidades":cant_comunidades, 'title': 'Comunidades'} # al final enviamos esto 
  return render (request,'map.html',data)
def comunidades(request):
  """
  Vista en donde se puede cargar las comunidades \n
  que van a recibir las donaciones
  """
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')
  if request.method=='POST':
    datos=request.POST 
    cant_comunidades=len(Comunidad.objects.all())
    orden=cant_comunidades +1 # a medida que se agregan van al ultimo
    datos_comunidades=Comunidad(nombre=datos.get('nombre'),responsable=datos.get('responsable'),latitud=float(datos.get('latitud')),longitud=float(datos.get('longitud')),cantidad_packs=datos.get('cantidad_packs'),entregado=False,listo=False,telefono_responsable=datos.get('numero_telefono'),observacion=datos.get('observacion'),orden=orden )
    datos_comunidades.save()
    lista=consulta_datos()
    cant_comunidades=len(Comunidad.objects.all())
    data = {"geo": lista,"cantidad_comunidades":cant_comunidades} # al final enviamos esto 
    return render(request,'comunidades.html',data)
  else:
    lista=consulta_datos()
    cant_comunidades=len(Comunidad.objects.all())
    data = {"geo": lista,"cantidad_comunidades":cant_comunidades} # al final enviamos esto 
    return render(request,'comunidades.html',data)

@csrf_exempt 
def actualizar_orden(request):
  """
  Actualiza el orden de las comunidades(para saber el orden de entrega)
  """
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')
  if request.method=='POST':
    lista= request.POST.getlist('listaCom[]')
    print(lista)
    for a in lista: #recorremos la lista para cambiar el orden 
       datos=Comunidad.objects.filter(nombre=a ).update(orden=lista.index(a)+1)
    data={"mensaje": "post recibido"}
  else:
    data={"mensaje": "No enviaste un post "}
  return JsonResponse(data)
#-------------------------FIN ADMINISTRACION-------------------------------



## -----------------------------DISTRIBUCION-------------------------------

#vista distribucion
def mapa_distribucion(request):
  """
  Vista en donde se administra ya la ultima etapa de la campanha,\n
  la distribucion de los kits.
  """
  if not request.user.is_authenticated:
      return render(request,'prueba_login.html')

  lista=consulta_datos()
  cant_comunidades=len(Comunidad.objects.all())
  data = {"geo": lista,"cantidad_comunidades":cant_comunidades, 'title': 'Comunidades'} # al final enviamos esto 
  return render(request,'map_distribucion.html',data)

#-----------------------FIN DISTRIBUCION--------------------------------

#No usado actualmente
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
  datos_comunidades=Comunidad.objects.all().order_by('orden')
  lista=[ ]
  for item in datos_comunidades:
      if item.entregado:
        entregado=1
      else:
        entregado=0
      cada_dato={ "id": item.id,"orden":item.orden,"nombre":item.nombre ,"responsable": item.responsable,"meta":item.cantidad_packs,
                    "telefono_responsable":item.telefono_responsable,"observacion":item.observacion,
                    "ubicacion": {"latitud": item.latitud,
                                    "longitud": item.longitud
                                  },
                           "entregado":entregado
                }
      lista.append(cada_dato) # agregamos a la lista
  return lista 