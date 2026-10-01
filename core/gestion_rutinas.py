from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal

from decimal import Decimal, InvalidOperation


from .models import (
    Cliente,
    Rutina,
    Ejercicio,
    EjercicioRutina,
)


def es_administrador(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_administrador)
def lista_rutinas(request):

    rutinas = (
        Rutina.objects
        .select_related("cliente")
        .prefetch_related("ejercicios_rutina__ejercicio")
        .order_by("-id")
    )

    return render(
        request,
        "core/gestion_rutinas.html",
        {
            "rutinas": rutinas,
        },
    )


@user_passes_test(es_administrador)
def nueva_rutina(request):

    clientes = Cliente.objects.order_by("nombre")
    ejercicios = Ejercicio.objects.order_by(
        "grupo_muscular",
        "nombre",
    )

    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        descripcion = request.POST.get("descripcion", "").strip()
        fecha_inicio = request.POST.get("fecha_inicio") or None
        cliente_id = request.POST.get("cliente")

        if not nombre:
            return render(
                request,
                "core/gestion_rutina_form.html",
                {
                    "titulo": "Nueva rutina",
                    "clientes": clientes,
                    "ejercicios": ejercicios,
                    "error": "El nombre de la rutina es obligatorio.",
                },
            )

        if not cliente_id:
            return render(
                request,
                "core/gestion_rutina_form.html",
                {
                    "titulo": "Nueva rutina",
                    "clientes": clientes,
                    "ejercicios": ejercicios,
                    "error": "Debes seleccionar un cliente.",
                },
            )

        cliente = get_object_or_404(
            Cliente,
            id=cliente_id,
        )

        rutina = Rutina.objects.create(
            nombre=nombre,
            cliente=cliente,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            activa=True,
        )

        # ----------------------------------------------------
        # EJERCICIOS
        # ----------------------------------------------------

        ejercicio_ids = request.POST.getlist("ejercicio_id")

        for posicion, ejercicio_id in enumerate(ejercicio_ids, start=1):

            if not ejercicio_id:
                continue

            ejercicio = get_object_or_404(
                Ejercicio,
                id=ejercicio_id,
            )

            series_texto = request.POST.get(
                f"series_{ejercicio_id}",
                "3",
            )

            repeticiones_texto = request.POST.get(
                f"repeticiones_{ejercicio_id}",
                "10",
            )

            peso_texto = request.POST.get(
                f"peso_{ejercicio_id}",
                "",
            ).strip()

            descanso_texto = request.POST.get(
                f"descanso_{ejercicio_id}",
                "60",
            )


            try:
                series = int(series_texto)
            except ValueError:
                series = 3


            try:
                repeticiones = int(repeticiones_texto)
            except ValueError:
                repeticiones = 10


            try:
                descanso = int(descanso_texto)
            except ValueError:
                descanso = 60


            peso = None

            if peso_texto:

                try:
                    peso = Decimal(
                        peso_texto.replace(",", ".")
                    )
                except InvalidOperation:
                    peso = None


            EjercicioRutina.objects.create(
                rutina=rutina,
                ejercicio=ejercicio,
                series=max(series, 1),
                repeticiones=max(repeticiones, 1),
                peso=peso,
                descanso=max(descanso, 0),
                orden=posicion,
            )


        return redirect(
            "rutina_detalle",
            rutina_id=rutina.id,
        )


    return render(
        request,
        "core/gestion_rutina_form.html",
        {
            "titulo": "Nueva rutina",
            "clientes": clientes,
            "ejercicios": ejercicios,
        },
    )


@user_passes_test(es_administrador)
def detalle_rutina(request, rutina_id):

    rutina = get_object_or_404(
        Rutina.objects
        .select_related("cliente")
        .prefetch_related(
            "ejercicios_rutina__ejercicio"
        ),
        id=rutina_id,
    )

    ejercicios_rutina = rutina.ejercicios_rutina.all().order_by(
        "orden",
        "id",
    )

    return render(
        request,
        "core/gestion_rutina_detalle.html",
        {
            "rutina": rutina,
            "ejercicios_rutina": ejercicios_rutina,
        },
    )


@user_passes_test(es_administrador)
def eliminar_rutina(request, rutina_id):

    rutina = get_object_or_404(
        Rutina,
        id=rutina_id,
    )

    if request.method == "POST":

        rutina.delete()

        return redirect("gestion_rutinas")


    return render(
        request,
        "core/gestion_rutina_eliminar.html",
        {
            "rutina": rutina,
        },
    )

@user_passes_test(es_administrador)
def editar_rutina(request, rutina_id):

    rutina = get_object_or_404(
        Rutina.objects
        .select_related("cliente")
        .prefetch_related(
            "ejercicios_rutina__ejercicio"
        ),
        id=rutina_id,
    )

    clientes = Cliente.objects.order_by("nombre")

    ejercicios = Ejercicio.objects.order_by(
        "grupo_muscular",
        "nombre",
    )

    ejercicios_actuales = {
        item.ejercicio_id: item
        for item in rutina.ejercicios_rutina.all()
    }


    if request.method == "POST":

        nombre = request.POST.get(
            "nombre",
            "",
        ).strip()

        descripcion = request.POST.get(
            "descripcion",
            "",
        ).strip()

        fecha_inicio = (
            request.POST.get("fecha_inicio")
            or None
        )

        cliente_id = request.POST.get(
            "cliente"
        )


        if not nombre:

            return render(
                request,
                "core/gestion_rutina_editar.html",
                {
                    "rutina": rutina,
                    "clientes": clientes,
                    "ejercicios": ejercicios,
                    "ejercicios_actuales": ejercicios_actuales,
                    "error": "El nombre de la rutina es obligatorio.",
                },
            )


        if not cliente_id:

            return render(
                request,
                "core/gestion_rutina_editar.html",
                {
                    "rutina": rutina,
                    "clientes": clientes,
                    "ejercicios": ejercicios,
                    "ejercicios_actuales": ejercicios_actuales,
                    "error": "Debes seleccionar un cliente.",
                },
            )


        cliente = get_object_or_404(
            Cliente,
            id=cliente_id,
        )


        rutina.nombre = nombre
        rutina.descripcion = descripcion
        rutina.fecha_inicio = fecha_inicio
        rutina.cliente = cliente

        rutina.save()


        # ----------------------------------------------------
        # EJERCICIOS SELECCIONADOS
        # ----------------------------------------------------

        ejercicio_ids = request.POST.getlist(
            "ejercicio_id"
        )


        # Eliminar los ejercicios que ya no fueron seleccionados

        EjercicioRutina.objects.filter(
            rutina=rutina
        ).exclude(
            ejercicio_id__in=ejercicio_ids
        ).delete()


        # Crear o actualizar ejercicios

        for posicion, ejercicio_id in enumerate(
            ejercicio_ids,
            start=1,
        ):

            if not ejercicio_id:
                continue


            ejercicio = get_object_or_404(
                Ejercicio,
                id=ejercicio_id,
            )


            series_texto = request.POST.get(
                f"series_{ejercicio_id}",
                "3",
            )

            repeticiones_texto = request.POST.get(
                f"repeticiones_{ejercicio_id}",
                "10",
            )

            peso_texto = request.POST.get(
                f"peso_{ejercicio_id}",
                "",
            ).strip()

            descanso_texto = request.POST.get(
                f"descanso_{ejercicio_id}",
                "60",
            )


            try:
                series = max(
                    int(series_texto),
                    1,
                )
            except ValueError:
                series = 3


            try:
                repeticiones = max(
                    int(repeticiones_texto),
                    1,
                )
            except ValueError:
                repeticiones = 10


            try:
                descanso = max(
                    int(descanso_texto),
                    0,
                )
            except ValueError:
                descanso = 60


            peso = None

            if peso_texto:

                try:

                    peso = Decimal(
                        peso_texto.replace(
                            ",",
                            ".",
                        )
                    )

                except InvalidOperation:

                    peso = None


            item, creado = (
                EjercicioRutina.objects.get_or_create(
                    rutina=rutina,
                    ejercicio=ejercicio,
                    defaults={
                        "series": series,
                        "repeticiones": repeticiones,
                        "peso": peso,
                        "descanso": descanso,
                        "orden": posicion,
                    },
                )
            )


            if not creado:

                item.series = series
                item.repeticiones = repeticiones
                item.peso = peso
                item.descanso = descanso
                item.orden = posicion

                item.save()


        return redirect(
            "rutina_detalle",
            rutina_id=rutina.id,
        )


    return render(
        request,
        "core/gestion_rutina_editar.html",
        {
            "rutina": rutina,
            "clientes": clientes,
            "ejercicios": ejercicios,
            "ejercicios_actuales": ejercicios_actuales,
        },
    )

# ============================================================
# ADMINISTRAR EJERCICIOS DE UNA RUTINA
# ============================================================

@login_required
@user_passes_test(es_administrador)
def gestionar_ejercicios_rutina(request, rutina_id):

    from django.shortcuts import get_object_or_404

    rutina = get_object_or_404(
        Rutina.objects.select_related("cliente"),
        id=rutina_id,
    )

    ejercicios = Ejercicio.objects.order_by(
        "grupo_muscular",
        "nombre",
    )

    ejercicios_rutina = (
        EjercicioRutina.objects
        .filter(rutina=rutina)
        .select_related("ejercicio")
        .order_by("orden", "id")
    )


    if request.method == "POST":

        ejercicio_id = request.POST.get(
            "ejercicio"
        )

        series_texto = request.POST.get(
            "series",
            "3",
        )

        repeticiones_texto = request.POST.get(
            "repeticiones",
            "10",
        )

        peso_texto = request.POST.get(
            "peso",
            "",
        ).strip()

        descanso_texto = request.POST.get(
            "descanso",
            "60",
        )

        orden_texto = request.POST.get(
            "orden",
            "",
        )


        if not ejercicio_id:

            return render(
                request,
                "core/gestion_rutina_ejercicios.html",
                {
                    "rutina": rutina,
                    "ejercicios": ejercicios,
                    "ejercicios_rutina": ejercicios_rutina,
                    "error": "Debes seleccionar un ejercicio.",
                },
            )


        ejercicio = get_object_or_404(
            Ejercicio,
            id=ejercicio_id,
        )


        # ----------------------------------------------------
        # EVITAR DUPLICAR EL MISMO EJERCICIO
        # ----------------------------------------------------

        if EjercicioRutina.objects.filter(
            rutina=rutina,
            ejercicio=ejercicio,
        ).exists():

            return render(
                request,
                "core/gestion_rutina_ejercicios.html",
                {
                    "rutina": rutina,
                    "ejercicios": ejercicios,
                    "ejercicios_rutina": ejercicios_rutina,
                    "error": (
                        "Ese ejercicio ya pertenece a esta rutina."
                    ),
                },
            )


        # ----------------------------------------------------
        # CONVERTIR VALORES
        # ----------------------------------------------------

        try:
            series = max(
                int(series_texto),
                1,
            )
        except (ValueError, TypeError):
            series = 3


        try:
            repeticiones = max(
                int(repeticiones_texto),
                1,
            )
        except (ValueError, TypeError):
            repeticiones = 10


        try:
            descanso = max(
                int(descanso_texto),
                0,
            )
        except (ValueError, TypeError):
            descanso = 60


        peso = None

        if peso_texto:

            try:


                peso = Decimal(
                    peso_texto.replace(
                        ",",
                        ".",
                    )
                )

            except Exception:

                peso = None


        if orden_texto:

            try:
                orden = max(
                    int(orden_texto),
                    1,
                )
            except (ValueError, TypeError):
                orden = (
                    EjercicioRutina.objects
                    .filter(rutina=rutina)
                    .count()
                    + 1
                )

        else:

            orden = (
                EjercicioRutina.objects
                .filter(rutina=rutina)
                .count()
                + 1
            )


        # ----------------------------------------------------
        # CREAR
        # ----------------------------------------------------

        EjercicioRutina.objects.create(
            rutina=rutina,
            ejercicio=ejercicio,
            series=series,
            repeticiones=repeticiones,
            peso=peso,
            descanso=descanso,
            orden=orden,
        )


        return redirect(
            "gestionar_ejercicios_rutina",
            rutina_id=rutina.id,
        )


    return render(
        request,
        "core/gestion_rutina_ejercicios.html",
        {
            "rutina": rutina,
            "ejercicios": ejercicios,
            "ejercicios_rutina": ejercicios_rutina,
        },
    )


# ============================================================
# EDITAR EJERCICIO DENTRO DE UNA RUTINA
# ============================================================

@login_required
@user_passes_test(es_administrador)
def editar_ejercicio_rutina(
    request,
    rutina_id,
    ejercicio_rutina_id,
):

    from django.shortcuts import get_object_or_404

    rutina = get_object_or_404(
        Rutina,
        id=rutina_id,
    )

    item = get_object_or_404(
        EjercicioRutina.objects.select_related(
            "ejercicio"
        ),
        id=ejercicio_rutina_id,
        rutina=rutina,
    )


    if request.method == "POST":

        series_texto = request.POST.get(
            "series",
            "3",
        )

        repeticiones_texto = request.POST.get(
            "repeticiones",
            "10",
        )

        peso_texto = request.POST.get(
            "peso",
            "",
        ).strip()

        descanso_texto = request.POST.get(
            "descanso",
            "60",
        )

        orden_texto = request.POST.get(
            "orden",
            "1",
        )


        try:
            item.series = max(
                int(series_texto),
                1,
            )
        except (ValueError, TypeError):
            item.series = 3


        try:
            item.repeticiones = max(
                int(repeticiones_texto),
                1,
            )
        except (ValueError, TypeError):
            item.repeticiones = 10


        try:
            item.descanso = max(
                int(descanso_texto),
                0,
            )
        except (ValueError, TypeError):
            item.descanso = 60


        try:
            item.orden = max(
                int(orden_texto),
                1,
            )
        except (ValueError, TypeError):
            item.orden = 1


        item.peso = None

        if peso_texto:

            try:


                item.peso = Decimal(
                    peso_texto.replace(
                        ",",
                        ".",
                    )
                )

            except Exception:

                item.peso = None


        item.save()


        return redirect(
            "gestionar_ejercicios_rutina",
            rutina_id=rutina.id,
        )


    return render(
        request,
        "core/gestion_rutina_ejercicio_editar.html",
        {
            "rutina": rutina,
            "item": item,
        },
    )


# ============================================================
# ELIMINAR EJERCICIO DE UNA RUTINA
# ============================================================

@login_required
@user_passes_test(es_administrador)
def eliminar_ejercicio_rutina(
    request,
    rutina_id,
    ejercicio_rutina_id,
):

    from django.shortcuts import get_object_or_404

    rutina = get_object_or_404(
        Rutina,
        id=rutina_id,
    )

    item = get_object_or_404(
        EjercicioRutina.objects.select_related(
            "ejercicio"
        ),
        id=ejercicio_rutina_id,
        rutina=rutina,
    )


    if request.method == "POST":

        item.delete()

        return redirect(
            "gestionar_ejercicios_rutina",
            rutina_id=rutina.id,
        )


    return render(
        request,
        "core/gestion_rutina_ejercicio_eliminar.html",
        {
            "rutina": rutina,
            "item": item,
        },
    )