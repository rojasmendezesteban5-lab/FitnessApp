from django.urls import path

from .gestion_ejercicios import (
    lista_ejercicios,
    nuevo_ejercicio,
    editar_ejercicio,
    eliminar_ejercicio,
)


urlpatterns = [

    path(
        "",
        lista_ejercicios,
        name="gestion_ejercicios",
    ),

    path(
        "nuevo/",
        nuevo_ejercicio,
        name="nuevo_ejercicio",
    ),

    path(
        "<int:ejercicio_id>/editar/",
        editar_ejercicio,
        name="editar_ejercicio",
    ),

    path(
        "<int:ejercicio_id>/eliminar/",
        eliminar_ejercicio,
        name="eliminar_ejercicio",
    ),

]
