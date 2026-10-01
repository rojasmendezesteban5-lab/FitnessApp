from django.urls import path

from .gestion_rutinas import (
    gestionar_ejercicios_rutina,
    editar_ejercicio_rutina,
    eliminar_ejercicio_rutina,
    editar_rutina,
    lista_rutinas,
    nueva_rutina,
    detalle_rutina,
    eliminar_rutina,
)


urlpatterns = [

    path(
        "<int:rutina_id>/ejercicios/",
        gestionar_ejercicios_rutina,
        name="gestionar_ejercicios_rutina",
    ),

    path(
        "<int:rutina_id>/ejercicios/<int:ejercicio_rutina_id>/editar/",
        editar_ejercicio_rutina,
        name="editar_ejercicio_rutina",
    ),

    path(
        "<int:rutina_id>/ejercicios/<int:ejercicio_rutina_id>/eliminar/",
        eliminar_ejercicio_rutina,
        name="eliminar_ejercicio_rutina",
    ),



    path(
        "",
        lista_rutinas,
        name="gestion_rutinas",
    ),

    path(
        "nueva/",
        nueva_rutina,
        name="nueva_rutina",
    ),

    path(
        "<int:rutina_id>/editar/",
        editar_rutina,
        name="editar_rutina",
    ),

    path(
        "<int:rutina_id>/",
        detalle_rutina,
        name="rutina_detalle",
    ),

    path(
        "<int:rutina_id>/eliminar/",
        eliminar_rutina,
        name="eliminar_rutina",
    ),

]
