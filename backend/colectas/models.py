from django.utils import timezone

from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Corporacion(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    anio_graduacion = models.PositiveSmallIntegerField(unique=True, primary_key=True)
    
    def __str__(self):
        return str(self.anio_graduacion)

class Circulo(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)

class Donador_Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=1000)

    class Meta:
        constraints = [
            CheckConstraint(
                condition=Q(fecha_fin__gte=F('fecha_inicio')),
                name='check_fecha_fin'
            )
        ]
    
    def __str__(self):
        return str(self.nombre)

class Voluntario(models.Model):
    nombre = models.CharField(max_length=100)
    primer_ap = models.CharField(max_length=100)
    segundo_ap = models.CharField(max_length=100, null=True)
    telefono = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)
    rol = models.CharField(max_length=30)

class Donador(models.Model):
    nombre = models.CharField(max_length=100)
    primer_ap = models.CharField(max_length=100)
    segundo_ap = models.CharField(max_length=100, null=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)
    categoria = models.ForeignKey(Donador_Categoria.__name__, on_delete=models.CASCADE, related_name='id_categoria', db_column='categoria')
    anio_graduacion = models.PositiveSmallIntegerField(unique=True)
    id_clase = models.ForeignKey(Clase.__name__, on_delete=models.CASCADE, db_column='id_clase')
    id_corporacion = models.ForeignKey(Corporacion.__name__, on_delete=models.CASCADE, related_name="id_corporacion", db_column="id_corporacion")
    nombre_conyuge = models.CharField(max_length=201)
    id_corporacion_conyuge = models.ForeignKey(Corporacion.__name__, on_delete=models.CASCADE, related_name="id_corporacion_conyuge", db_column="id_corporacion_conyuge")
    
class AsistenciaEvento(models.Model):
    id_evento = models.ForeignKey(Evento.__name__, on_delete=models.CASCADE)
    id_donador = models.ForeignKey(Donador.__name__, on_delete=models.CASCADE)

class Garantia(models.Model):
    id_donador = models.ForeignKey(Donador.__name__, on_delete=models.CASCADE)
    id_evento = models.ForeignKey(Evento.__name__, on_delete=models.CASCADE)
    garantia = models.DecimalField(max_digits=12, decimal_places=2)
    pago_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    metodo_pago = models.CharField(max_length=50)
    numero_pagos = models.PositiveIntegerField(default=0)
    numero_tarjeta = models.CharField(max_length=20)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    id_circulo = models.ForeignKey(Circulo.__name__, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default='Pendiente')

class Pago(models.Model):
    id_garantia = models.ForeignKey(Garantia.__name__, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)

class Llamada(models.Model):
    id_voluntario = models.ForeignKey(Voluntario.__name__, on_delete=models.CASCADE)
    id_donador = models.ForeignKey(Donador.__name__, on_delete=models.CASCADE)
    id_garantia = models.ForeignKey(Garantia.__name__, on_delete=models.CASCADE)
    fecha = models.DateField()
    respuesta = models.CharField(max_length=50)
    observaciones = models.TextField(max_length=1000)

class Userio(AbstractUser):
    rol = models.CharField(max_length=255, default='usuario')
    date_joined = models.DateTimeField(default=timezone.now)
    pass