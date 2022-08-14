from django.http import HttpResponse
from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,"login/index.html")

def registro(request):

    if request.method== "POST":
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']

        user = User.objects.create_user(usuario,correo,contrasena)
        user.first_name = nombre
        user.last_name = apellido

        user.save()

        return redirect('ingreso')
    return render(request, "login/registro.html")


def ingreso(request):

    if request.method == 'POST':
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        user = authenticate(username=usuario, password=contrasena)

        if user is not None:
            login(request,user)
            nombre = user.first_name
            return render(request, "login/index.html", {'nombre': nombre})
        else:
            messages.error(request,"Datos erroneos")
            return redirect('home')

    return render(request, "login/ingreso.html")
def salida(request):
    logout(request)
    return redirect('home')
    pass