from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .models import Ejercicio, EjercicioRutina
from .gestion_clientes import es_administrador


@login_required
@user_passes_test(es_administrador)
def lista_ejercicios(request):

    ejercicios = Ejercicio.objects.all().order_by(
        "grupo_muscular",
        "nombre",
    )

    return render(
        request,
        "core/gestion_ejercicios.html",
        {
            "ejercicios": ejercicios,
        },
    )


@login_required
@user_passes_test(es_administrador)
def nuevo_ejercicio(request):

    if request.method == "POST":

        nombre = request.POST.get(
            "nombre",
            "",
        ).strip()

        grupo_muscular = request.POST.get(
            "grupo_muscular",
            "",
        ).strip()

        descripcion = request.POST.get(
            "descripcion",
            "",
        ).strip()

        instrucciones = request.POST.get(
            "instrucciones",
            "",
        ).strip()

        imagen = request.POST.get(
            "imagen",
            "",
        ).strip()

        video = request.POST.get(
            "video",
            "",
        ).strip()


        if not nombre:

            return render(
                request,
                "core/gestion_ejercicio_form.html",
                {
                    "modo": "nuevo",
                    "error": "El nombre del ejercicio es obligatorio.",
                    "datos": request.POST,
                },
            )


        if not grupo_muscular:

            return render(
                request,
                "core/gestion_ejercicio_form.html",
                {
                    "modo": "nuevo",
                    "error": "El grupo muscular es obligatorio.",
                    "datos": request.POST,
                },
            )


        Ejercicio.objects.create(
            nombre=nombre,
            grupo_muscular=grupo_muscular,
            descripcion=descripcion,
            instrucciones=instrucciones,
            imagen=imagen,
            video=video,
        )


        return redirect("gestion_ejercicios")


    return render(
        request,
        "core/gestion_ejercicio_form.html",
        {
            "modo": "nuevo",
        },
    )


@login_required
@user_passes_test(es_administrador)
def editar_ejercicio(request, ejercicio_id):

    ejercicio = get_object_or_404(
        Ejercicio,
        id=ejercicio_id,
    )


    if request.method == "POST":

        nombre = request.POST.get(
            "nombre",
            "",
        ).strip()

        grupo_muscular = request.POST.get(
            "grupo_muscular",
            "",
        ).strip()

        descripcion = request.POST.get(
            "descripcion",
            "",
        ).strip()

        instrucciones = request.POST.get(
            "instrucciones",
            "",
        ).strip()

        imagen = request.POST.get(
            "imagen",
            "",
        ).strip()

        video = request.POST.get(
            "video",
            "",
        ).strip()


        if not nombre:

            return render(
                request,
                "core/gestion_ejercicio_form.html",
                {
                    "modo": "editar",
                    "ejercicio": ejercicio,
                    "error": "El nombre del ejercicio es obligatorio.",
                },
            )


        if not grupo_muscular:

            return render(
                request,
                "core/gestion_ejercicio_form.html",
                {
                    "modo": "editar",
                    "ejercicio": ejercicio,
                    "error": "El grupo muscular es obligatorio.",
                },
            )


        ejercicio.nombre = nombre
        ejercicio.grupo_muscular = grupo_muscular
        ejercicio.descripcion = descripcion
        ejercicio.instrucciones = instrucciones
        ejercicio.imagen = imagen
        ejercicio.video = video

        ejercicio.save()


        return redirect("gestion_ejercicios")


    return render(
        request,
        "core/gestion_ejercicio_form.html",
        {
            "modo": "editar",
            "ejercicio": ejercicio,
        },
    )


@login_required
@user_passes_test(es_administrador)
def eliminar_ejercicio(request, ejercicio_id):

    ejercicio = get_object_or_404(
        Ejercicio,
        id=ejercicio_id,
    )


    usos = EjercicioRutina.objects.filter(
        ejercicio=ejercicio
    ).count()


    if request.method == "POST":

        if usos > 0:

            return render(
                request,
                "core/gestion_ejercicio_eliminar.html",
                {
                    "ejercicio": ejercicio,
                    "usos": usos,
                    "error": (
                        "No se puede eliminar este ejercicio "
                        "porque pertenece a una o más rutinas."
                    ),
                },
            )


        ejercicio.delete()

        return redirect(
            "gestion_ejercicios"
        )


    return render(
        request,
        "core/gestion_ejercicio_eliminar.html",
        {
            "ejercicio": ejercicio,
            "usos": usos,
        },
    )
