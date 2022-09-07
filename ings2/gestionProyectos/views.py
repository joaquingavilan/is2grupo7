from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionProyectos import models
from django.http import JsonResponse


# Create your views here.
def home(request):
    if not models.Formulario.objects.exists():
        crear_formularios()
    return render(request, "login/index.html")


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


def gestion_usuarios(request):
    lista_usuarios = models.Usuario.objects.all()
    lista_roles = models.UsuarioRol.objects.all()
    contexto = {
        "lista_usuarios": lista_usuarios,
        "usuario_rol": lista_roles
    }
    return render(request, "seguridad/usuarios.html", contexto)


def gestion_roles(request):
    lista_roles = models.Rol.objects.all()

    contexto = {
        "lista_roles": lista_roles
    }
    return render(request, "seguridad/roles.html", contexto)


def gestion_permisos(request):
    lista_permisos = models.Permiso.objects.all()
    contexto = {
        "lista_permisos": lista_permisos
    }
    return render(request, "seguridad/permisos.html", contexto)


def busq_usuarios(request):
    query_dict = request.GET.get("busq_usuario")
    usuario_encontrado = None
    if query_dict is not None:
        usuario_encontrado = models.Usuario.objects.get(nombre=query_dict)
    contexto = {
        "usuario": usuario_encontrado
    }
    return render(request, "seguridad/buscar_usuario.html", contexto)


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


def add_permiso(request):
    if request.method == "POST":
        nombre = request.POST['nombre']
        modulo = request.POST['modulo']
        formulario = models.Formulario.objects.get(id=int(request.POST['formulario'][0]))

        permiso = models.Permiso(nombre=nombre, modulo=modulo, id_formulario=formulario)
        permiso.save()
        return redirect('seguridad')
    formularios = models.Formulario.objects.all()
    id_nombre =[]
    for formu in formularios:
        id_nombre.append(str(formu.id) + '-' + formu.nombre)
    return render(request, "seguridad/add_permiso.html", {"formularios": id_nombre})


def add_rol(request):

    if request.method == "POST":
        nombre = request.POST['nombre']
        permisos = request.POST.getlist('permisos')
        rol = models.Rol(nombre=nombre)
        rol.save()
        for perm in permisos:
            permiso = models.Permiso.objects.get(id=perm)
            rol.permisos.add(permiso)
        return redirect('seguridad')
    permisos = models.Permiso.objects.all()
    return render(request, "seguridad/add_rol.html", {"permisos": permisos})


def mod_usuario(request):
    mostrar_usuarios = User.objects.all()
    return render(request, 'seguridad/mod_usuario.html', {"Usuario": mostrar_usuarios})


def alterar_permiso(request):
    formularios = models.Formulario.objects.all()
    if request.method == "POST":
        id_seleccionado = request.POST['permis']
        permiso_filtrado = models.Permiso.objects.get(id=id_seleccionado)
        if "mod" in request.POST:
            return render(request, "seguridad/mod_permiso.html",
                          {"permiso": permiso_filtrado, "formulario": formularios})
        elif "del" in request.POST:
            return render(request, "seguridad/del_permiso.html",
                          {"permiso": permiso_filtrado, "formulario": formularios})
    return render(request, "seguridad/mod_permiso.html")


def alterar_usuario(request):

    if request.method == "POST":

        id_seleccionado = request.POST['user']
        rol_user = models.Rol.objects.get(id_usuario=id_seleccionado)
        rol = rol_user.id_rol
        usuario_filtrado = models.Usuario.objects.get(id=id_seleccionado)
        if "mod" in request.POST:
            return render(request, "seguridad/mod_usuario.html",
                          {"usuario": usuario_filtrado, "rol": rol})
        elif "del" in request.POST:
            return render(request, "seguridad/del_usuario.html",
                          {"usuario": usuario_filtrado, "rol": rol})
    return render(request, "seguridad/mod_usuario.html")


def cambiar_permiso(request):
    if request.method == "POST":
        id_form = int(request.POST['formulario'][0])
        models.Permiso.objects.filter(id=(request.POST['id_cambio'])).update(nombre=request.POST['nombre'],
                                                                             modulo=request.POST['modulo'],
                                                                             id_formulario=models.Formulario.objects.get(id=id_form))
        return redirect('gestion_permisos')
    return render(request, "seguridad/permisos.html")


def eliminar_permiso(request):
    if request.method == "POST":
        models.Permiso.objects.filter(id=(request.POST['id_elim'])).delete()
        return redirect('gestion_permisos')
    return render(request, "seguridad/permisos.html")

def del_usuario(request):
    mostrar_usuarios = User.objects.all()
    return render(request, 'seguridad/del_usuario.html', {"Usuario": mostrar_usuarios}) #


def crear_formularios():
    nombres = ["Crear Usuario", "Crear Permiso", "Crear Rol", "Modificar Usuario", "Modificar Rol", "Modificar Permiso",
               "Eliminar Usuario", "Eliminar Permiso", "Eliminar Rol"]
    for nombre in nombres:
        form = models.Formulario(nombre=nombre)
        form.save()