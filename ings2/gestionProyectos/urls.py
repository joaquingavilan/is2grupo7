from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('registro',views.registro,name="registro"),
    path('ingreso', views.ingreso, name="ingreso"),
    path('salida', views.salida, name="salida"),
    path('seguridad', views.seguridad, name="seguridad"),
    path('inicio', views.inicio, name="inicio"),
    path('add_usuario', views.add_usuario, name="add_usuario"),
    path('mod_usuario', views.mod_usuario, name="mod_usuario"),
    path('del_usuario', views.del_usuario, name="del_usuario")
]
