from django.urls import path

from .gestion_clientes import (
    lista_clientes,
    detalle_cliente,
    nuevo_cliente,
    editar_cliente,
    eliminar_cliente,
)

urlpatterns = [
    path("", lista_clientes, name="gestion_clientes"),
    path("agregar/", nuevo_cliente, name="nuevo_cliente"),
    path("<int:cliente_id>/editar/", editar_cliente, name="editar_cliente"),
    path("<int:cliente_id>/eliminar/", eliminar_cliente, name="eliminar_cliente"),
]
