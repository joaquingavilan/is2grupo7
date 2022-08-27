from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionProyectos import models

# Create your views here.
def home(request):
    return render(request, "login/index.html")


def registro(request):
    if request.method == "POST":
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']
        u = models.Usuario(nombre=usuario, contrasena=contrasena)  # se guarda el usuario en la tabla Usuario, creada en el modelo
        u.save()

        user = User.objects.create_user(username=usuario, password=contrasena)
        user.save()                                                # se guarda en la tabla auth_user, propia de django

        return redirect('ingreso')
    return render(request, "login/registro.html")


def ingreso(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        user = authenticate(username=usuario, password=contrasena)

        if user is not None:
            login(request, user)
            nombre = user.first_name
            return render(request, "login/index.html", {'nombre': nombre})
        else:
            messages.error(request, "Datos erroneos")
            return redirect('home')

    return render(request, "login/ingreso.html")


def salida(request):
    logout(request)
    return redirect('home')
    pass


# revision de codigo

def seguridad(request):
    return render(request, "seguridad/seguridad.html")


def inicio(request):
    return render(request, "login/index.html")


def add_usuario(request):
    if request.method == "POST":
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']
        u = models.Usuario(nombre=usuario, contrasena=contrasena) #se guarda el usuario en la tabla Usuario, creada en el modelo
        u.save()
        user = User.objects.create_user(username=usuario, password=contrasena) #se guarda el usuario en la tabla auth_user (proveida por django)
        user.save()

        return redirect('seguridad')
    return render(request, "seguridad/add_usuario.html")


def mod_usuario(request):
    mostrar_usuarios = User.objects.all()
    return render(request, 'seguridad/mod_usuario.html', {"Usuario": mostrar_usuarios})


def del_usuario(request):
    mostrar_usuarios = User.objects.all()
    return render(request, 'seguridad/del_usuario.html', {"Usuario": mostrar_usuarios}) #