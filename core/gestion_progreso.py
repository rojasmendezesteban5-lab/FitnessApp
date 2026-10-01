
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Cliente, Ejercicio, Progreso


def es_administrador(user):
    return user.is_staff


# ============================================================
# LISTA DE PROGRESO
# ============================================================

@login_required
@user_passes_test(es_administrador)
def lista_progreso(request):

    cliente_id = request.GET.get("cliente")

    registros = Progreso.objects.select_related(
        "cliente",
        "ejercicio"
    ).order_by(
        "-fecha",
        "-id"
    )

    if cliente_id:
        registros = registros.filter(
            cliente_id=cliente_id
        )

    clientes = Cliente.objects.all().order_by("nombre")

    return render(
        request,
        "core/gestion_progreso.html",
        {
            "registros": registros,
            "clientes": clientes,
            "cliente_seleccionado": cliente_id,
        }
    )


# ============================================================
# NUEVO PROGRESO
# ============================================================

@login_required
@user_passes_test(es_administrador)
def nuevo_progreso(request):

    clientes = Cliente.objects.all().order_by("nombre")

    ejercicios = Ejercicio.objects.all().order_by(
        "nombre"
    )

    if request.method == "POST":

        cliente_id = request.POST.get("cliente")
        ejercicio_id = request.POST.get("ejercicio")

        peso = request.POST.get("peso")
        repeticiones = request.POST.get("repeticiones")
        peso_ejercicio = request.POST.get("peso_ejercicio")
        notas = request.POST.get("notas")

        cliente = get_object_or_404(
            Cliente,
            id=cliente_id
        )

        ejercicio = None

        if ejercicio_id:
            ejercicio = get_object_or_404(
                Ejercicio,
                id=ejercicio_id
            )

        Progreso.objects.create(

            cliente=cliente,

            ejercicio=ejercicio,

            peso=peso or None,

            repeticiones=repeticiones or None,

            peso_ejercicio=peso_ejercicio or None,

            notas=notas or ""
        )

        return redirect(
            "gestion_progreso"
        )

    return render(
        request,
        "core/gestion_progreso_form.html",
        {
            "titulo": "Nuevo registro de progreso",
            "clientes": clientes,
            "ejercicios": ejercicios,
            "progreso": None,
        }
    )


# ============================================================
# EDITAR PROGRESO
# ============================================================

@login_required
@user_passes_test(es_administrador)
def editar_progreso(request, progreso_id):

    progreso = get_object_or_404(
        Progreso,
        id=progreso_id
    )

    clientes = Cliente.objects.all().order_by("nombre")

    ejercicios = Ejercicio.objects.all().order_by(
        "nombre"
    )

    if request.method == "POST":

        cliente_id = request.POST.get("cliente")
        ejercicio_id = request.POST.get("ejercicio")

        progreso.cliente = get_object_or_404(
            Cliente,
            id=cliente_id
        )

        if ejercicio_id:

            progreso.ejercicio = get_object_or_404(
                Ejercicio,
                id=ejercicio_id
            )

        else:

            progreso.ejercicio = None

        peso = request.POST.get("peso")
        repeticiones = request.POST.get("repeticiones")
        peso_ejercicio = request.POST.get("peso_ejercicio")
        notas = request.POST.get("notas")

        progreso.peso = peso or None

        progreso.repeticiones = (
            repeticiones or None
        )

        progreso.peso_ejercicio = (
            peso_ejercicio or None
        )

        progreso.notas = notas or ""

        progreso.save()

        return redirect(
            "gestion_progreso"
        )

    return render(
        request,
        "core/gestion_progreso_form.html",
        {
            "titulo": "Editar registro de progreso",
            "clientes": clientes,
            "ejercicios": ejercicios,
            "progreso": progreso,
        }
    )


# ============================================================
# ELIMINAR PROGRESO
# ============================================================

@login_required
@user_passes_test(es_administrador)
def eliminar_progreso(request, progreso_id):

    progreso = get_object_or_404(
        Progreso,
        id=progreso_id
    )

    if request.method == "POST":

        progreso.delete()

        return redirect(
            "gestion_progreso"
        )

    return render(
        request,
        "core/gestion_progreso_eliminar.html",
        {
            "progreso": progreso
        }
    )
