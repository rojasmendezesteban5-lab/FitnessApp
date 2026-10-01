from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction

from .models import (
    Cliente,
    Rutina,
    Ejercicio,
    EjercicioRutina,
    Progreso,
)


# =========================================================
# PÁGINA INICIAL
# =========================================================

def inicio(request):
    return render(request, "core/inicio.html")


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("/dashboard/")
        return redirect("/")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:

            auth_login(request, usuario)

            if usuario.is_staff:
                return redirect("/dashboard/")

            return redirect("/")

        messages.error(
            request,
            "Usuario o contraseña incorrectos."
        )

    return render(
        request,
        "core/login.html"
    )


# =========================================================
# PERFIL
# =========================================================

@login_required
def perfil(request):

    if request.user.is_staff:
        return redirect("/dashboard/")

    cliente = request.user.cliente

    return render(
        request,
        "core/perfil.html",
        {
            "cliente": cliente
        }
    )


# =========================================================
# RUTINA DEL CLIENTE
# =========================================================

@login_required
def rutina(request):

    if request.user.is_staff:
        return redirect("/dashboard/")

    cliente = request.user.cliente

    rutina = cliente.rutinas.filter(
        activa=True
    ).first()

    ejercicios_rutina = []

    if rutina:
        ejercicios_rutina = rutina.ejercicios_rutina.select_related(
            "ejercicio"
        ).order_by("orden")

    return render(
        request,
        "core/rutina.html",
        {
            "rutina": rutina,
            "ejercicios_rutina": ejercicios_rutina,
        }
    )


# =========================================================
# EJERCICIOS PÚBLICOS
# =========================================================

@login_required
def ejercicios(request):

    if request.user.is_staff:
        return redirect("/dashboard/")

    return redirect("/rutina/")
@login_required
def progreso(request):

    if request.user.is_staff:
        return redirect("/dashboard/")

    cliente = request.user.cliente

    if request.method == "POST":

        peso = request.POST.get("peso")
        repeticiones = request.POST.get("repeticiones")
        peso_ejercicio = request.POST.get("peso_ejercicio")
        ejercicio_id = request.POST.get("ejercicio")
        notas = request.POST.get("notas")

        ejercicio = None

        if ejercicio_id:
            ejercicio = Ejercicio.objects.filter(
                id=ejercicio_id
            ).first()

        Progreso.objects.create(
            cliente=cliente,
            ejercicio=ejercicio,
            peso=peso or None,
            repeticiones=repeticiones or None,
            peso_ejercicio=peso_ejercicio or None,
            notas=notas or ""
        )

        return redirect("/progreso/")

    progresos = cliente.progresos.select_related(
        "ejercicio"
    ).all().order_by("fecha", "id")

    fechas = []
    pesos = []

    for registro in progresos:

        if registro.peso is not None:

            fechas.append(
                registro.fecha.strftime("%d/%m/%Y")
            )

            pesos.append(
                float(registro.peso)
            )

    peso_actual = None
    peso_inicial = None
    cambio_peso = None

    if pesos:

        peso_inicial = pesos[0]
        peso_actual = pesos[-1]

        cambio_peso = round(
            peso_actual - peso_inicial,
            2
        )

    ejercicios_progreso = {}

    for registro in progresos:

        if registro.ejercicio:

            nombre = registro.ejercicio.nombre

            if nombre not in ejercicios_progreso:
                ejercicios_progreso[nombre] = []

            ejercicios_progreso[nombre].append({
                "fecha": registro.fecha.strftime("%d/%m/%Y"),
                "repeticiones": registro.repeticiones,
                "peso_ejercicio": registro.peso_ejercicio,
                "notas": registro.notas,
            })

    return render(
        request,
        "core/progreso.html",
        {
            "progresos": progresos,
            "fechas": fechas,
            "pesos": pesos,
            "peso_actual": peso_actual,
            "peso_inicial": peso_inicial,
            "cambio_peso": cambio_peso,
            "ejercicios_progreso": ejercicios_progreso,
        }
    )


# =========================================================
# ADMINISTRADOR
# =========================================================

def es_administrador(user):

    return user.is_staff


@login_required
@user_passes_test(es_administrador)
def dashboard(request):

    total_clientes = Cliente.objects.count()
    total_ejercicios = Ejercicio.objects.count()
    total_rutinas = Rutina.objects.count()
    total_progresos = Progreso.objects.count()

    clientes = Cliente.objects.all().order_by("nombre")

    return render(
        request,
        "core/dashboard.html",
        {
            "total_clientes": total_clientes,
            "total_ejercicios": total_ejercicios,
            "total_rutinas": total_rutinas,
            "total_progresos": total_progresos,
            "clientes": clientes,
        }
    )


# =========================================================
# ADMINISTRAR CLIENTES
# =========================================================

@login_required
@user_passes_test(es_administrador)
def lista_clientes_admin(request):

    clientes = Cliente.objects.all().order_by("nombre")

    return render(
        request,
        "core/administrar_clientes.html",
        {
            "clientes": clientes
        }
    )


# =========================================================
# AGREGAR CLIENTE
# =========================================================

@login_required
@user_passes_test(es_administrador)
def agregar_cliente_admin(request):

    if request.method == "POST":

        nombre = request.POST.get(
            "nombre",
            ""
        ).strip()

        correo = request.POST.get(
            "correo",
            ""
        ).strip().lower()

        telefono = request.POST.get(
            "telefono",
            ""
        ).strip()

        edad = request.POST.get(
            "edad",
            ""
        ).strip()

        peso = request.POST.get(
            "peso",
            ""
        ).strip()

        altura = request.POST.get(
            "altura",
            ""
        ).strip()

        objetivo = request.POST.get(
            "objetivo",
            ""
        ).strip()

        notas = request.POST.get(
            "notas",
            ""
        ).strip()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        password2 = request.POST.get(
            "password2",
            ""
        )


        # ---------------------------------------------
        # VALIDACIONES
        # ---------------------------------------------

        if not nombre:
            messages.error(
                request,
                "Debes ingresar el nombre del cliente."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if not correo:
            messages.error(
                request,
                "Debes ingresar el correo electrónico."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if not username:
            messages.error(
                request,
                "Debes ingresar un nombre de usuario."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if not password:
            messages.error(
                request,
                "Debes ingresar una contraseña."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if password != password2:

            messages.error(
                request,
                "Las contraseñas no coinciden."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Ese nombre de usuario ya existe."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if User.objects.filter(
            email=correo
        ).exists():

            messages.error(
                request,
                "Ya existe un usuario con ese correo."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        if Cliente.objects.filter(
            correo=correo
        ).exists():

            messages.error(
                request,
                "Ya existe un cliente con ese correo."
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


        # ---------------------------------------------
        # CREAR USUARIO + CLIENTE
        # ---------------------------------------------

        try:

            with transaction.atomic():

                usuario = User.objects.create_user(
                    username=username,
                    email=correo,
                    password=password,
                    first_name=nombre,
                )

                usuario.is_staff = False
                usuario.is_superuser = False

                usuario.save()


                cliente = Cliente.objects.create(
                    usuario=usuario,
                    nombre=nombre,
                    correo=correo,
                    telefono=telefono,
                    edad=edad or None,
                    peso=peso or None,
                    altura=altura or None,
                    objetivo=objetivo,
                    notas=notas,
                )


            messages.success(
                request,
                f"Cliente {cliente.nombre} creado correctamente. "
                f"Usuario: {username}"
            )

            return redirect(
                "/admin/clientes/"
            )

        except Exception as error:

            messages.error(
                request,
                f"No se pudo crear el cliente: {error}"
            )

            return redirect(
                "/admin/clientes/agregar/"
            )


    return render(
        request,
        "core/agregar_cliente.html"
    )


# =========================================================
# ADMINISTRAR EJERCICIOS
# =========================================================

@login_required
@user_passes_test(es_administrador)
def lista_ejercicios_admin(request):

    ejercicios = Ejercicio.objects.all().order_by(
        "nombre"
    )

    return render(
        request,
        "core/administrar_ejercicios.html",
        {
            "ejercicios": ejercicios
        }
    )


# =========================================================
# AGREGAR EJERCICIO
# =========================================================

@login_required
@user_passes_test(es_administrador)
def agregar_ejercicio_admin(request):

    if request.method == "POST":

        datos = {}

        campos = [
            "nombre",
            "grupo_muscular",
            "descripcion",
            "instrucciones",
            "video",
        ]

        campos_modelo = {
            campo.name
            for campo in Ejercicio._meta.fields
        }

        for campo in campos:

            if campo in campos_modelo:

                valor = request.POST.get(
                    campo,
                    ""
                ).strip()

                datos[campo] = valor

        Ejercicio.objects.create(
            **datos
        )

        messages.success(
            request,
            "Ejercicio creado correctamente."
        )

        return redirect(
            "/admin/ejercicios/"
        )


    campos_modelo = []

    campos_permitidos = [
        "nombre",
        "grupo_muscular",
        "descripcion",
        "instrucciones",
        "video",
    ]

    nombres = {

        "nombre":
            "Nombre del ejercicio",

        "grupo_muscular":
            "Grupo muscular",

        "descripcion":
            "Descripción",

        "instrucciones":
            "Instrucciones",

        "video":
            "Video",
    }


    for campo in Ejercicio._meta.fields:

        if campo.name in campos_permitidos:

            campos_modelo.append(
                {
                    "nombre": campo.name,

                    "label": nombres.get(
                        campo.name,
                        campo.name.replace(
                            "_",
                            " "
                        ).title()
                    ),
                }
            )


    return render(
        request,
        "core/agregar_ejercicio.html",
        {
            "campos": campos_modelo
        }
    )


# =========================================================
# COMPATIBILIDAD
# =========================================================

agregar_ejercicio = agregar_ejercicio_admin

administrar_ejercicios = lista_ejercicios_admin

administrar_clientes = lista_clientes_admin

agregar_cliente = agregar_cliente_admin

def login(request):

    mensaje = ""

    if request.method == "POST":

        usuario = request.POST.get("usuario")
        password = request.POST.get("password")

        usuario_autenticado = authenticate(
            request,
            username=usuario,
            password=password
        )

        if usuario_autenticado is not None:

            auth_login(
                request,
                usuario_autenticado
            )

            if usuario_autenticado.is_staff:
                return redirect("/dashboard/")

            return redirect("/perfil/")

        mensaje = "Usuario o contraseña incorrectos."

    return render(
        request,
        "core/login.html",
        {
            "mensaje": mensaje
        }
    )




# =========================================================
# CERRAR SESIÓN
# =========================================================

def logout(request):
    auth_logout(request)
    return redirect("/login/")



# ==========================================
# CLIENTE - MARCAR EJERCICIO COMPLETADO
# ==========================================

@login_required
def completar_ejercicio(request, ejercicio_rutina_id):

    if request.user.is_staff:
        return redirect("/dashboard/")

    cliente = request.user.cliente

    ejercicio_rutina = get_object_or_404(
        EjercicioRutina,
        id=ejercicio_rutina_id,
        rutina__cliente=cliente
    )

    ejercicio_rutina.completado = True
    ejercicio_rutina.save()

    return redirect("/rutina/")

# ==========================================
# CLIENTE - MARCAR EJERCICIO COMPLETADO
# ==========================================

@login_required
def completar_ejercicio(request, ejercicio_rutina_id):

    if request.user.is_staff:
        return redirect("/dashboard/")

    cliente = request.user.cliente

    ejercicio_rutina = get_object_or_404(
        EjercicioRutina,
        id=ejercicio_rutina_id,
        rutina__cliente=cliente
    )

    ejercicio_rutina.completado = True
    ejercicio_rutina.save()

    return redirect("/rutina/")



