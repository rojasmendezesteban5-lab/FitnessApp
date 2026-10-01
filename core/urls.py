from .gestion_clientes import lista_clientes, detalle_cliente, nuevo_cliente, editar_cliente, eliminar_cliente
from django.urls import path, include, include
from . import views

urlpatterns = [
    path("gestion/progreso/", include("core.gestion_progreso_urls")),
    path(
        "gestion/ejercicios/",
        include("core.gestion_ejercicios_urls"),
    ),
    path("rutinas/", include("core.gestion_rutinas_urls")),
    path("clientes/", lista_clientes, name="clientes"),
    path(
        "clientes/<int:cliente_id>/",
        detalle_cliente,
        name="cliente_detalle",
    ),
    path(
        "gestion/",
        include("core.gestion_urls"),
    ),

    path("", views.inicio, name="inicio"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("rutina/", views.rutina, name="rutina"),
    path("rutina/completar/<int:ejercicio_rutina_id>/", views.completar_ejercicio, name="completar_ejercicio"),
    path("ejercicios/", views.ejercicios, name="ejercicios"),
    path("progreso/", views.progreso, name="progreso"),

    path(
        "admin/ejercicios/",
        views.lista_ejercicios_admin,
        name="lista_ejercicios_admin",
    ),

    path(
        "admin/ejercicios/agregar/",
        views.agregar_ejercicio_admin,
        name="agregar_ejercicio_admin",
    ),
]


