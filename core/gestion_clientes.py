from decimal import Decimal, InvalidOperation

from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cliente


def es_administrador(user):
    return user.is_authenticated and user.is_staff


def convertir_decimal(valor):
    """
    Convierte valores como:
        80
        80.00
        80,00

    a Decimal correctamente.

    Si viene vacío, devuelve None.
    """

    if valor is None:
        return None

    valor = str(valor).strip()

    if not valor:
        return None

    valor = valor.replace(",", ".")

    try:
        return Decimal(valor)
    except (InvalidOperation, ValueError):
        return None


@user_passes_test(es_administrador)
def lista_clientes(request):

    clientes = (
        Cliente.objects
        .select_related("usuario")
        .order_by("nombre")
    )

    return render(
        request,
        "core/gestion_clientes.html",
        {
            "clientes": clientes,
        },
    )


@user_passes_test(es_administrador)
def detalle_cliente(request, cliente_id):

    cliente = get_object_or_404(
        Cliente.objects.select_related("usuario"),
        id=cliente_id,
    )

    rutinas = cliente.rutinas.all().order_by("-id")
    progresos = cliente.progresos.all().order_by("-fecha")

    return render(
        request,
        "core/gestion_cliente_detalle.html",
        {
            "cliente": cliente,
            "rutinas": rutinas,
            "progresos": progresos,
        },
    )


@user_passes_test(es_administrador)
def nuevo_cliente(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        edad_texto = request.POST.get("edad", "").strip()
        peso_texto = request.POST.get("peso", "").strip()
        altura_texto = request.POST.get("altura", "").strip()

        objetivo = request.POST.get("objetivo", "").strip()
        notas = request.POST.get("notas", "").strip()

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()


        # --------------------------------------------
        # VALIDACIONES BASICAS
        # --------------------------------------------

        if not nombre or not correo:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Agregar cliente",
                    "error": "El nombre y el correo son obligatorios.",
                    "cliente": None,
                },
            )


        if Cliente.objects.filter(correo=correo).exists():

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Agregar cliente",
                    "error": "Ya existe un cliente con ese correo.",
                    "cliente": None,
                },
            )


        # --------------------------------------------
        # CONVERSION DE NUMEROS
        # --------------------------------------------

        edad = None

        if edad_texto:

            try:
                edad = int(edad_texto)
            except ValueError:

                return render(
                    request,
                    "core/gestion_cliente_form.html",
                    {
                        "titulo": "Agregar cliente",
                        "error": "La edad debe ser un número entero.",
                        "cliente": None,
                    },
                )


        peso = convertir_decimal(peso_texto)
        altura = convertir_decimal(altura_texto)


        if peso_texto and peso is None:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Agregar cliente",
                    "error": "El peso debe ser un número válido. Ejemplo: 80.00",
                    "cliente": None,
                },
            )


        if altura_texto and altura is None:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Agregar cliente",
                    "error": "La altura debe ser un número válido. Ejemplo: 1.75",
                    "cliente": None,
                },
            )


        # --------------------------------------------
        # USUARIO DEL CLIENTE
        # --------------------------------------------

        usuario = None

        if username:

            if User.objects.filter(username=username).exists():

                return render(
                    request,
                    "core/gestion_cliente_form.html",
                    {
                        "titulo": "Agregar cliente",
                        "error": "Ese nombre de usuario ya existe.",
                        "cliente": None,
                    },
                )


            if not password:

                return render(
                    request,
                    "core/gestion_cliente_form.html",
                    {
                        "titulo": "Agregar cliente",
                        "error": "Si escribes un nombre de usuario, también debes indicar una contraseña.",
                        "cliente": None,
                    },
                )


            usuario = User.objects.create_user(
                username=username,
                email=correo,
                password=password,
            )


        # --------------------------------------------
        # CREAR CLIENTE
        # --------------------------------------------

        cliente = Cliente.objects.create(
            usuario=usuario,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            edad=edad,
            peso=peso,
            altura=altura,
            objetivo=objetivo,
            notas=notas,
        )


        return redirect(
            "cliente_detalle",
            cliente_id=cliente.id,
        )


    return render(
        request,
        "core/gestion_cliente_form.html",
        {
            "titulo": "Agregar cliente",
            "cliente": None,
        },
    )


@user_passes_test(es_administrador)
def editar_cliente(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id,
    )


    if request.method == "POST":

        nombre = request.POST.get("nombre", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()

        edad_texto = request.POST.get("edad", "").strip()
        peso_texto = request.POST.get("peso", "").strip()
        altura_texto = request.POST.get("altura", "").strip()

        objetivo = request.POST.get("objetivo", "").strip()
        notas = request.POST.get("notas", "").strip()


        # --------------------------------------------
        # VALIDACIONES
        # --------------------------------------------

        if not nombre or not correo:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Editar cliente",
                    "error": "El nombre y el correo son obligatorios.",
                    "cliente": cliente,
                },
            )


        existe = (
            Cliente.objects
            .filter(correo=correo)
            .exclude(id=cliente.id)
            .exists()
        )


        if existe:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Editar cliente",
                    "error": "Ya existe otro cliente con ese correo.",
                    "cliente": cliente,
                },
            )


        # --------------------------------------------
        # EDAD
        # --------------------------------------------

        edad = None

        if edad_texto:

            try:
                edad = int(edad_texto)
            except ValueError:

                return render(
                    request,
                    "core/gestion_cliente_form.html",
                    {
                        "titulo": "Editar cliente",
                        "error": "La edad debe ser un número entero.",
                        "cliente": cliente,
                    },
                )


        # --------------------------------------------
        # PESO Y ALTURA
        # --------------------------------------------

        peso = convertir_decimal(peso_texto)
        altura = convertir_decimal(altura_texto)


        if peso_texto and peso is None:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Editar cliente",
                    "error": "El peso debe ser un número válido. Ejemplo: 80.00",
                    "cliente": cliente,
                },
            )


        if altura_texto and altura is None:

            return render(
                request,
                "core/gestion_cliente_form.html",
                {
                    "titulo": "Editar cliente",
                    "error": "La altura debe ser un número válido. Ejemplo: 1.75",
                    "cliente": cliente,
                },
            )


        # --------------------------------------------
        # GUARDAR CAMBIOS
        # --------------------------------------------

        cliente.nombre = nombre
        cliente.correo = correo
        cliente.telefono = telefono
        cliente.edad = edad
        cliente.peso = peso
        cliente.altura = altura
        cliente.objetivo = objetivo
        cliente.notas = notas

        cliente.save()


        # Actualizar correo del usuario si existe

        if cliente.usuario:

            cliente.usuario.email = correo
            cliente.usuario.save()


        return redirect(
            "cliente_detalle",
            cliente_id=cliente.id,
        )


    return render(
        request,
        "core/gestion_cliente_form.html",
        {
            "titulo": "Editar cliente",
            "cliente": cliente,
        },
    )


@user_passes_test(es_administrador)
def eliminar_cliente(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id,
    )


    if request.method == "POST":

        usuario = cliente.usuario

        cliente.delete()

        if usuario:

            usuario.delete()


        return redirect("clientes")


    return render(
        request,
        "core/gestion_cliente_eliminar.html",
        {
            "cliente": cliente,
        },
    )
