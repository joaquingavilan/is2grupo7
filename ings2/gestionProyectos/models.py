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
    nombre = models.CharField(max_length=50)
    contrasena = models.CharField(max_length=50)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)


class Proyecto(models.Model):
    class Estados(models.TextChoices):
        ENC = "EN CURSO", "En Curso"
        FIN = "FINALIZADO", "Finalizado"
    nombre = models.CharField(max_length=50)
    usuarios = models.ManyToManyField(Usuario)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    estado = models.CharField(choices=Estados.choices, max_length=50, default=Estados.ENC)


class Backlog(models.Model):
    nombre = models.CharField(max_length=50)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)


class UserStory(models.Model):
    nombre = models.CharField(max_length=50)
    backlog = models.ForeignKey(Backlog, on_delete=models.CASCADE)
    usuarios = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateField
