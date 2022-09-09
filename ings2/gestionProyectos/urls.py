from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('ingreso', views.ingreso, name="ingreso"),
    path('salida', views.salida, name="salida"),
    path('seguridad', views.seguridad, name="seguridad"),
    path('gestion_usuarios', views.gestion_usuarios, name="gestion_usuarios"),
    path('gestion_roles', views.gestion_roles, name="gestion_roles"),
    path('gestion_permisos', views.gestion_permisos, name="gestion_permisos"),
    path('busq_usuarios', views.busq_usuarios),
    path('inicio', views.inicio, name="inicio"),
    path('add_usuario', views.add_usuario, name="add_usuario"),
    path('add_rol', views.add_rol, name="add_rol"),
    path('add_permiso', views.add_permiso, name="add_permiso"),
    path('mod_usuario', views.mod_usuario, name="mod_usuario"),
    path('alterar_permiso', views.alterar_permiso, name="alterar_permiso"),
    path('alterar_rol', views.alterar_rol, name="alterar_rol"),
    path('alterar_usuario', views.alterar_usuario, name="alterar_usuario"),
    path('cambiar_permiso', views.cambiar_permiso, name="cambiar_permiso"),
    path('cambiar_rol', views.cambiar_rol, name="cambiar_rol"),
    path('cambiar_usuario', views.cambiar_usuario, name="cambiar_usuario"),
    path('eliminar_permiso', views.eliminar_permiso, name="eliminar_permiso"),
    path('eliminar_rol', views.eliminar_rol, name="eliminar_rol"),
    path('eliminar_usuario', views.eliminar_usuario, name="eliminar_usuario")
]
