
from django.urls import path

from .gestion_progreso import (
    lista_progreso,
    nuevo_progreso,
    editar_progreso,
    eliminar_progreso,
)

urlpatterns = [
    path("", lista_progreso, name="gestion_progreso"),
    path("nuevo/", nuevo_progreso, name="nuevo_progreso"),
    path("<int:progreso_id>/editar/", editar_progreso, name="editar_progreso"),
    path("<int:progreso_id>/eliminar/", eliminar_progreso, name="eliminar_progreso"),
]
