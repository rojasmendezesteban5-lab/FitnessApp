from django.contrib import admin
from django.urls import path, include

from core import views


urlpatterns = [

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =====================================================
    # CLIENTES
    # =====================================================

    path(
        "admin/clientes/",
        views.lista_clientes_admin,
        name="lista_clientes_admin"
    ),

    path(
        "admin/clientes/agregar/",
        views.agregar_cliente_admin,
        name="agregar_cliente_admin"
    ),

    path(
        "admin/clientes/agregar",
        views.agregar_cliente_admin,
        name="agregar_cliente_admin_sin_slash"
    ),


    # =====================================================
    # EJERCICIOS
    # =====================================================

    path(
        "admin/ejercicios/",
        views.lista_ejercicios_admin,
        name="lista_ejercicios_admin"
    ),

    path(
        "admin/ejercicios/agregar/",
        views.agregar_ejercicio_admin,
        name="agregar_ejercicio_admin"
    ),

    path(
        "admin/ejercicios/agregar",
        views.agregar_ejercicio_admin,
        name="agregar_ejercicio_admin_sin_slash"
    ),


    # =====================================================
    # ADMINISTRADOR DJANGO
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),


    # =====================================================
    # RUTAS DE CORE
    # =====================================================

    path(
        "",
        include("core.urls")
    ),
]