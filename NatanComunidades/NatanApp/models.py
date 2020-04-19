from django.db import models
from django.utils import timezone

# Create your models here.
class Medida(models.Model):
  simbolo = models.CharField(max_length=45)
  def __str__(self):
    return self.simbolo

class Articulo(models.Model):
  medida = models.ForeignKey(Medida, on_delete=models.PROTECT)
  nombre = models.CharField(max_length=45)
  def __str__(self):
    return self.nombre

class Donacion(models.Model):
  donante = models.CharField(max_length=150, default='')
  fecha = models.DateField(default=timezone.now())
  imagen = models.ImageField(upload_to='images', default='images/none.jpg')
  observaciones = models.TextField(default='', blank=True)
  def __str__(self):
    return self.donante + ' - ' + str(self.fecha)

class Donacionxarticulo(models.Model):
  donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE)
  articulo = models.ForeignKey(Articulo, on_delete=models.PROTECT)
  cantidad = models.IntegerField()
  def __str__(self):
    return '{0}: {1} - {2}'.format(self.donacion, str(self.cantidad), self.articulo)
