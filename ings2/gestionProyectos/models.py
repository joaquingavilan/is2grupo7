from django.db import models
from django.contrib.auth.models import User


# Create your models here.




class Formulario(models.Model):
    nombre = models.CharField(max_length=50)


class Permiso(models.Model):
    class Modulos(models.TextChoices):
        SEG = "SEGURIDAD", "Seguridad"
        PROY = "PROYECTO", "Proyecto"
        DASH = "DASHBOARD", "Dashboard"

    nombre = models.CharField(max_length=50)
    modulo = models.CharField(choices=Modulos.choices, max_length=50)
    id_formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE)


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    permisos = models.ManyToManyField(Permiso)

class Usuario(models.Model):
    # no se necesita id pues es generado automaticamente como primary key e incremental
    nombre = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


