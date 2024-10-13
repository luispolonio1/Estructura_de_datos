from django.db import models
from datetime import datetime

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    cedula = models.CharField(max_length=50)
    edad = models.IntegerField(default=0)
    fecha_registro = models.DateField(default=datetime.now)
    def __str__(self):
        return f"{self.nombre} - {self.cedula} - {self.edad}"



