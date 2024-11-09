from django.core.validators import MinLengthValidator
from django.db import models
from datetime import datetime

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=12,validators=[MinLengthValidator(8)])
    edad = models.IntegerField(default=0)
    fecha_registro = models.DateField(default=datetime.now)
    atendido = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.nombre} -{self.apellido}-{self.cedula} - {self.edad}"


class UsuarioAtendido(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=12,validators=[MinLengthValidator(8)])
    edad = models.IntegerField()
    fecha_registro = models.DateField(default=datetime.now,)

    def __str__(self):
        return f"{self.nombre} -{self.apellido}- {self.cedula} - {self.edad}"

class RegistroHoy(models.Model):
    fecha = models.DateField(default=datetime.now)
    usuarios = models.ManyToManyField(UsuarioAtendido, related_name='registro_diario')

    def __str__(self):
        return f"Registro de {self.fecha} - {self.usuarios.count()} usuarios"

