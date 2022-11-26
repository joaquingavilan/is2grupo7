from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from gestionProyectos import models
from django.http import JsonResponse
from datetime import datetime, timedelta, date


# Create your views here.
def home(request):
    if not models.Formulario.objects.exists():
        crear_formularios()                         #se cargan los formularios (son estaticos, no se crean dentro del sistema pero deben actualizrse a medida que se agregan funciones)
    verificar_sprints()
    return render(request, "login/ingreso.html")      #se muestra la pagina de inicio


def verificar_sprints():
    sprints = models.Sprint.objects.all()
    for sp in sprints:
        if sp.fecha_inicio is not None:
            if (datetime.now().date() > sp.fecha_fin) and (sp.estado == "EN CURSO"): #selecciona los sprints activos cuya duracion terminó
                backlog = sp.backlog                                                                                #selecciona el backlog del sprint seleccionado
                sprints = models.Sprint.objects.filter(backlog=backlog)                                             #selecciona todos los sprints del backlog seleccionado
                sp.estado = "FINALIZADO"
                sp.save()
                for spr in sprints:
                    if spr.fecha_inicio is None:                                                                    #selecciona el sprint con fecha de inicio null
                        spr.fecha_inicio = sp.fecha_inicio + timedelta(days=1)                                     #cambia la fecha de inicio al dia siguiente de la fecha de fin
                        spr.save()
                        spr.fecha_fin = spr.fecha_inicio + timedelta(days=spr.duracion)                               #actualiza la fecha de fin del sprint
                        spr.save()
                        spr.estado = "EN CURSO"                                                                    #cambia el estado a En Curso
                        spr.save()
                        user_stories = models.UserStory.objects.filter(sprint=sp)                                   #obtiene las user_stories del sprint anterior
                        for us in user_stories:
                            if us.estado != "FINALIZADO":                                                           #si el estado no es finalizado, mueve la US al siguiente sprint
                                us.sprint = spr
                                us.save()


def ingreso(request):
    if request.method == 'POST':
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']

        user = authenticate(username=usuario, password=contrasena)  #se utiliza una funcion de la libreria User para ver si la contraseña y user estan correctos

        if user is not None:                                        #si el usuario es correcto
            login(request, user)                                    #se loguea
            nombre = user.first_name                                #se pasa el nombre para mostrar mensaje de bienvenida
            return render(request, "login/index.html", {'nombre': nombre}) #pasando el nombre al html para poder mostrar
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
    lista_usuarios = models.Usuario.objects.all()           #se obtiene la lista de usuarios del sistema
    contexto = {
        "lista_usuarios": lista_usuarios
    }
    return render(request, "seguridad/usuarios/usuarios.html", contexto)        #se pasa la lista de usuarios al html para poder visualizar


def gestion_roles(request):
    lista_roles = models.Rol.objects.all() #obtener lista de roles

    contexto = {
        "lista_roles": lista_roles
    }
    return render(request, "seguridad/roles/roles.html", contexto) #pasar lista de roles


def gestion_permisos(request):
    lista_permisos = models.Permiso.objects.all() #obtener lista de permisos
    contexto = {
        "lista_permisos": lista_permisos
    }
    return render(request, "seguridad/permisos/permisos.html", contexto) #pasar lista de permisos


def inicio(request):
    return render(request, "login/index.html")


def add_usuario(request):
    roles = models.Rol.objects.all() #obtenemos los roles
    if request.method == "POST":
        usuario = request.POST['usuario']
        contrasena = request.POST['contrasena']
        rol = models.Rol.objects.get(id=request.POST['rol']) #extraemos el rol que coincide con el rol proveniente de la request
        u = models.Usuario(nombre=usuario, contrasena=contrasena, rol=rol) #se guarda el usuario en la tabla Usuario, creada en el modelo
        u.save()
        user = User.objects.create_user(username=usuario, password=contrasena) #se guarda el usuario en la tabla auth_user (proveida por django)
        user.save()
        return redirect('seguridad')
    return render(request, "seguridad/usuarios/add_usuario.html", {"roles": roles}) #si no hay un formulario POST se pasa la lista de roles para poder asignar uno al usuario nuevo


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
    return render(request, "seguridad/permisos/add_permiso.html", {"formularios": id_nombre})


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
    return render(request, "seguridad/roles/add_rol.html", {"permisos": permisos})


def mod_usuario(request):
    mostrar_usuarios = User.objects.all()
    return render(request, 'seguridad/usuarios/mod_usuario.html', {"Usuario": mostrar_usuarios})


def alterar_permiso(request):
    formularios = models.Formulario.objects.all()
    if request.method == "POST":
        id_seleccionado = request.POST['permis']
        permiso_filtrado = models.Permiso.objects.get(id=id_seleccionado)
        if "mod" in request.POST:
            return render(request, "seguridad/permisos/mod_permiso.html",
                          {"permiso": permiso_filtrado, "formulario": formularios})
        elif "del" in request.POST:
            return render(request, "seguridad/permisos/del_permiso.html",
                          {"permiso": permiso_filtrado, "formulario": formularios})
    return render(request, "seguridad/permisos/mod_permiso.html")


def alterar_rol(request):
    permisos = models.Permiso.objects.all()
    if request.method == "POST":
        id_seleccionado = request.POST['rol']
        rol_filtrado = models.Rol.objects.get(id=id_seleccionado)
        if "mod" in request.POST:
            return render(request, "seguridad/roles/mod_rol.html",
                          {"rol": rol_filtrado, "permisos": permisos})
        elif "del" in request.POST:
            return render(request, "seguridad/roles/del_rol.html",
                          {"rol": rol_filtrado})
    return render(request, "seguridad/roles/mod_rol.html")


def alterar_usuario(request):
    roles = models.Rol.objects.all()
    if request.method == "POST":
        id_seleccionado = request.POST['user']
        usuario_filtrado = models.Usuario.objects.get(id=id_seleccionado)
        if "mod" in request.POST:
            return render(request, "seguridad/usuarios/mod_usuario.html",
                          {"usuario": usuario_filtrado, "roles": roles})
        elif "del" in request.POST:
            return render(request, "seguridad/usuarios/del_usuario.html",
                          {"usuario": usuario_filtrado})
    return render(request, "seguridad/usuarios/mod_usuario.html")


def cambiar_permiso(request):
    if request.method == "POST":
        id_form = int(request.POST['formulario'][0])
        models.Permiso.objects.filter(id=(request.POST['id_cambio'])).update(nombre=request.POST['nombre'],
                                                                             modulo=request.POST['modulo'],
                                                                             id_formulario=models.Formulario.objects.get(id=id_form))
        return redirect('gestion_permisos')
    return render(request, "seguridad/permisos/permisos.html")


def cambiar_rol(request):
    if request.method == "POST":
        models.Rol.objects.filter(id=(request.POST['id_cambio'])).update(nombre=request.POST['nombre'])
        rol_modificado = models.Rol.objects.get(id=(request.POST['id_cambio']))
        if not not request.POST.getlist('permisos'):
            rol_modificado.permisos.clear()
            permisos = request.POST.getlist('permisos')
            for perm in permisos:
                permiso = models.Permiso.objects.get(id=perm)
                rol_modificado.permisos.add(permiso)
        return redirect('gestion_roles')
    return render(request, "seguridad/roles/roles.html")


def cambiar_usuario(request):
    if request.method == "POST":
        rol = models.Rol.objects.get(id=(request.POST['rol']))
        models.Usuario.objects.filter(id=(request.POST['id_cambio'])).update(nombre=request.POST['nombre'],
                                                                             contrasena=request.POST['contrasena'],
                                                                             rol=rol)
        return redirect('gestion_usuarios')
    return render(request, "seguridad/usuarios/usuarios.html")


def eliminar_permiso(request):
    if request.method == "POST":
        models.Permiso.objects.filter(id=(request.POST['id_elim'])).delete()
        return redirect('gestion_permisos')
    return render(request, "seguridad/permisos/permisos.html")


def eliminar_rol(request):
    if request.method == "POST":
        models.Rol.objects.filter(id=(request.POST['id_elim'])).delete()
        return redirect('gestion_roles')
    return render(request, "seguridad/roles/roles.html")


def eliminar_usuario(request):
    if request.method == "POST":
        models.Usuario.objects.filter(id=(request.POST['id_elim'])).delete()
        return redirect('gestion_usuarios')
    return render(request, 'seguridad/usuarios/del_usuario.html')


def crear_formularios():
    nombres = ["Crear Usuario", "Crear Permiso", "Crear Rol", "Modificar Usuario", "Modificar Rol", "Modificar Permiso",
               "Eliminar Usuario", "Eliminar Permiso", "Eliminar Rol"]
    for nombre in nombres:
        form = models.Formulario(nombre=nombre)
        form.save()


def gestion_proyectos(request):
    proyectos = models.Proyecto.objects.all()
    contexto = {
        "lista_proyectos": proyectos
    }
    return render(request, 'proyecto/proyectos.html', contexto)


def add_proyecto(request):
    usuarios = models.Usuario.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        nombre_backlog = request.POST['backlog']
        fecha_inicio = request.POST['inicio']
        proyecto = models.Proyecto(nombre=nombre, fecha_inicio=fecha_inicio)
        proyecto.save()
        usuarios = request.POST.getlist('usuarios')
        for user in usuarios:
            us = models.Usuario.objects.get(id=user)
            proyecto.usuarios.add(us)
        backlog = models.Backlog(nombre=nombre_backlog, proyecto=proyecto)
        backlog.save()
        return redirect(gestion_proyectos)
    return render(request, 'proyecto/add_proyecto.html', {"usuarios": usuarios})


def ver_proyecto(request):
    proyecto = models.Proyecto.objects.get(id=request.POST['proyecto'])
    usuarios = models.Usuario.objects.all()
    return render(request, 'proyecto/ver_proyecto.html', {"proyecto": proyecto, "usuarios": usuarios})


def eliminar_proyecto(request):
    proyecto = models.Proyecto.objects.get(id=request.POST['proyect'])
    #backlog = models.Backlog.objects.get(proyecto=proyecto)
    #models.UserStory.objects.filter(backlog=backlog).delete()
    #models.Backlog.objects.filter(proyecto=proyecto).delete()
    models.Proyecto.objects.filter(id=request.POST['proyect']).delete()
    return redirect(gestion_proyectos)

def eliminar_user_proyecto(request):
    usuarios = models.Usuario.objects.all()
    proyecto = models.Proyecto.objects.get(id=request.POST['proyecto'])
    proyecto.usuarios.remove(models.Usuario.objects.get(id=request.POST['usuario']))
    proyecto = models.Proyecto.objects.get(id=request.POST['proyecto'])
    return render(request, 'proyecto/ver_proyecto.html', {"proyecto": proyecto, "usuarios": usuarios})


def add_user_proyecto(request):
    usuarios = models.Usuario.objects.all()
    proyecto = models.Proyecto.objects.get(id=request.POST['proy'])
    usuario = models.Usuario.objects.get(id=request.POST['usuario'])
    for user in proyecto.usuarios.all():
        if user.id == usuario.id:
            return render(request, 'proyecto/ver_proyecto.html', {"proyecto": proyecto, "usuarios": usuarios})
    proyecto.usuarios.add(usuario)
    return render(request, 'proyecto/ver_proyecto.html', {"proyecto": proyecto, "usuarios": usuarios})


def ver_backlog(request):
    proyecto = models.Proyecto.objects.get(id=request.POST['proyec'])
    backlog = models.Backlog.objects.get(proyecto=proyecto)
    sprints = models.Sprint.objects.filter(backlog=backlog)
    return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})


def ver_sprint(request):
    backlog = models.Backlog.objects.get(id=request.POST['back'])
    sprint = models.Sprint.objects.get(id=request.POST['sp'])
    user_stories = models.UserStory.objects.filter(sprint=sprint)
    return render(request, 'proyecto/ver_sprint.html', {"backlog":backlog,"sprint":sprint,"user_stories": user_stories})


def add_us(request):
    if request.method == 'GET':
        sprint = models.Sprint.objects.get(id=request.GET['sp'])
        proyecto = sprint.backlog.proyecto
        usuarios = proyecto.usuarios.all()
        return render(request, 'proyecto/add_us.html', {"sprint": sprint, "usuarios": usuarios})
    elif request.method == 'POST':
        nombre = request.POST['nombre']
        usuario = models.Usuario.objects.get(id=request.POST['usuario'])
        sprint = models.Sprint.objects.get(id=request.POST['sp'])
        fecha_inicio = request.POST['inicio']
        user_story = models.UserStory(nombre=nombre, usuario=usuario, sprint=sprint,fecha_inicio=fecha_inicio)
        user_story.save()
        backlog = models.Backlog.objects.get(id=sprint.backlog.id)
        sprints = models.Sprint.objects.filter(backlog=backlog)
        return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})



def add_sp(request):
    if request.method == 'POST':
        backlog = models.Backlog.objects.get(id=request.POST['backl'])
        sprint = models.Sprint(duracion=request.POST['duracion'],backlog=backlog)
        sprint.save()
        sprints = models.Sprint.objects.filter(backlog=backlog)
        return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})
    backlog = models.Backlog.objects.get(id=request.GET['backl'])
    return render(request, 'proyecto/add_sp.html', {"backlog": backlog})


def finalizar_sprint(request):
    if request.method == 'POST':
        sprint = models.Sprint.objects.get(id=request.POST['sp'])
        backlog = sprint.backlog
        sprints = models.Sprint.objects.filter(backlog=backlog)
        user_stories = models.UserStory.objects.filter(sprint=sprint)
        if sprint.estado == "FINALIZADO":
            return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})
        for us in user_stories:
            if (us.estado == "EN CURSO") or (us.estado == "PENDIENTE"):
                return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})
        sprint.estado = "FINALIZADO"
        sprint.fecha_fin = datetime.now().date()
        sprint.save()
        for sp in sprints:
            if sp.estado == "PENDIENTE":
                return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})
        proyecto = backlog.proyecto
        proyecto.estado = "FINALIZADO"
        proyecto.save()
        return render(request, "login/index.html")


def iniciar_sprint(request):
    if request.method == 'POST':
        sprint = models.Sprint.objects.get(id=request.POST['sp'])
        backlog = sprint.backlog
        sprints = models.Sprint.objects.filter(backlog=backlog)
        for sp in sprints:
            if sp.estado == "EN CURSO":
                return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})
        sprint.estado = "EN CURSO"
        sprint.fecha_inicio = datetime.now().date()
        sprint.fecha_fin = sprint.fecha_inicio + timedelta(days=sprint.duracion)
        sprint.save()
        sprints = models.Sprint.objects.filter(backlog=sprint.backlog)
        return render(request, 'proyecto/ver_backlog.html', {"backlog": backlog, "sprints": sprints})


def cambiar_estado_us(request):
    if request.method == 'POST':
        id_us = request.POST['us']
        us = models.UserStory.objects.get(id=id_us)
        if us.estado == 'PENDIENTE':
            us.estado = 'EN CURSO'
            us.save()
        elif us.estado == 'EN CURSO':
            us.estado = 'FINALIZADO'
            us.save()
        backlog = us.sprint.backlog
        sprint = us.sprint
        user_stories = models.UserStory.objects.filter(sprint=sprint)
        return render(request, 'proyecto/ver_sprint.html',
                      {"backlog": backlog, "sprint": sprint, "user_stories": user_stories})


def ver_us(request):
    if request.method == 'POST':
        id_us = request.POST['us']
        us = models.UserStory.objects.get(id=id_us)
        return render(request, 'proyecto/ver_us.html',{"us": us})