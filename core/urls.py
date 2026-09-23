from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("clientes/", views.clientes, name="clientes"),
    path("clientes/agregar/", views.agregar_cliente, name="agregar_cliente"),
    path("clientes/<int:cliente_id>/", views.ver_cliente, name="ver_cliente"),
    path("clientes/<int:cliente_id>/rutina/agregar/", views.agregar_rutina, name="agregar_rutina"),
    path("rutinas/<int:rutina_id>/ejercicio/agregar/", views.agregar_ejercicio_rutina, name="agregar_ejercicio_rutina"),
    path("rutina/", views.rutina, name="rutina"),
    path("rutina/completar/<int:ejercicio_rutina_id>/", views.completar_ejercicio, name="completar_ejercicio"),
    path("perfil/", views.perfil, name="perfil"),
    path("ejercicios/", views.ejercicios, name="ejercicios"),
    path("progreso/", views.progreso, name="progreso"),
    path("login/", views.login, name="login"),
]
