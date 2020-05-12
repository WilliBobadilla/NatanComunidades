from django.db import models
from django.utils import timezone

from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
#creamos el grupo si es que no existe en django y dar permisos 
#g1 = Group.objects.create(name='pruebanomas')
#tenemos tres tipos de usuarios, con sus respectivos permisos 
"""
superusuario:    puede hacer de todo
registrador:   
            APP                   Tabla             permisos
             NatanApp --------  articulo  -------- add,change,delete,view
             NatanApp --------  donacion  -------- add,change,delete,view
             NatanApp --------  donacionxarticulo  -------- add,change,delete,view
             NatanApp --------  medida  -------- add,change,delete,view

Administrador: 
            APP                   Tabla             permisos
             NatanApp --------  Comunidad  -------- add,change,delete,view
Distribuidor: 
            APP                   Tabla             permisos
             NatanApp --------  Comunidad --------  change,view               
"""




# Create your models here.
class Medida(models.Model):
  simbolo = models.CharField(max_length=45, unique=True)
  print('Se creó un medida')
  def __str__(self):
    return self.simbolo

class Articulo(models.Model):
  medida = models.ForeignKey(Medida, on_delete=models.PROTECT)
  nombre = models.CharField(max_length=45, unique=True)
  print('Se creó un articulo')
  def __str__(self):
    return self.nombre

class Donacion(models.Model):
  donante = models.CharField(max_length=150, default='')
  fecha = models.DateField(default=timezone.now())
  imagen = models.ImageField(upload_to='', null=True)
  observaciones = models.TextField(default='', blank=True)
  def __str__(self):
    return self.donante + ' - ' + str(self.fecha)

class Donacionxarticulo(models.Model):
  donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE)
  articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
  cantidad = models.IntegerField()
  def __str__(self):
    return '{0}: {1} - {2}'.format(self.donacion, str(self.cantidad), self.articulo)

class Comunidad(models.Model):
  id=models.AutoField(primary_key=True)
  orden=models.IntegerField(default=0)
  nombre = models.CharField(max_length=150, default='')
  responsable = models.CharField(max_length=150, default='')
  cantidad_packs= models.IntegerField(default=0)
  #localizacion = models.CharField(max_length=150, default='')
  #cambio el models a integerfield para mejor manejo de las ubicaciones
  latitud= models.FloatField(default=-45.54)
  longitud= models.FloatField(default=-45.54)
  telefono_responsable=models.CharField(max_length=30, default='')
  entregado = models.BooleanField() # para saber si se entrego o no 
  listo = models.BooleanField() #para saber si ya esta para entregarse 
  observacion= models.TextField(default=" ",max_length=500)


if __name__ == "__main__":
    pass