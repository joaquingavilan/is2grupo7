from django.contrib import admin
from django.urls import path, include
from gestionProyectos import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("gestionProyectos.urls")),
    path('mod_usuario', views.mod_usuario)
]
