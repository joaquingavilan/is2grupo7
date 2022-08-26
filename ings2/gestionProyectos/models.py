from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Usuario(models.Model):
    # no se necesita id pues es generado automaticamente como primary key e incremental
    nombre = models.CharField(User.username)
    contrasena = models.CharField(User.password)

    def __str__(self):
        return self.id


class Formulario(models.Model):
    nombre = models.CharField()


class Permiso(models.Model):
    class Modulos(models.TextChoices):
        SEG = "SEGURIDAD", "Seguridad"
        PROY = "PROYECTO", "Proyecto"
        DASH = "DASHBOARD", "Dashboard"

    nombre = models.CharField()
    modulo = models.CharField(choices=Modulos.choices)
    id_formulario = models.ForeignKey(Formulario)


class Rol(models.Model):
    nombre = models.CharField()
    id_permiso = models.ForeignKey(Permiso)


class UsuarioRol(models.Model):
    id_usuario = models.ForeignKey(Usuario)
    id_rol = models.ForeignKey(Rol)
