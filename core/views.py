from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Cliente, Rutina, Ejercicio, EjercicioRutina, Progreso


# ==========================================
# PÁGINA INICIAL
# ==========================================

def inicio(request):
    return render(request, "core/inicio.html")


# ==========================================
# CLIENTE - RUTINA
# ==========================================

@login_required
def rutina(request):

    cliente = request.user.cliente
    rutina = cliente.rutinas.filter(activa=True).first()

    return render(
        request,
        "core/rutina.html",
        {"rutina": rutina}
    )


# ==========================================
# CLIENTE - MARCAR EJERCICIO COMPLETADO
# ==========================================

@login_required
def completar_ejercicio(request, ejercicio_rutina_id):

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
# CLIENTE - PERFIL
# ==========================================

@login_required
def perfil(request):

    cliente = request.user.cliente

    return render(
        request,
        "core/perfil.html",
        {"cliente": cliente}
    )


# ==========================================
# CLIENTE - EJERCICIOS
# ==========================================

@login_required
def ejercicios(request):

    ejercicios = Ejercicio.objects.all()

    return render(
        request,
        "core/ejercicios.html",
        {"ejercicios": ejercicios}
    )


# ==========================================
# CLIENTE - PROGRESO
# ==========================================

@login_required
def progreso(request):

    cliente = request.user.cliente

    if request.method == "POST":

        peso = request.POST.get("peso")
        repeticiones = request.POST.get("repeticiones")
        peso_ejercicio = request.POST.get("peso_ejercicio")
        notas = request.POST.get("notas")

        Progreso.objects.create(
            cliente=cliente,
            peso=peso or None,
            repeticiones=repeticiones or None,
            peso_ejercicio=peso_ejercicio or None,
            notas=notas
        )

        return redirect("/progreso/")

    progresos = cliente.progresos.all().order_by("fecha")

    fechas = []
    pesos = []

    for registro in progresos:

        if registro.peso is not None:

            fechas.append(
                registro.fecha.strftime("%d/%m/%Y")
            )

            pesos.append(float(registro.peso))

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
        }
    )


# ==========================================
# COMPROBAR ADMINISTRADOR
# ==========================================

def es_administrador(user):
    return user.is_staff


# ==========================================
# DASHBOARD
# ==========================================

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


# ==========================================
# LISTA DE CLIENTES
# ==========================================

@login_required
@user_passes_test(es_administrador)
def clientes(request):

    clientes = Cliente.objects.all().order_by("nombre")

    return render(
        request,
        "core/clientes.html",
        {
            "clientes": clientes
        }
    )


# ==========================================
# AGREGAR CLIENTE
# ==========================================

@login_required
@user_passes_test(es_administrador)
def agregar_cliente(request):

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        edad = request.POST.get("edad")
        peso = request.POST.get("peso")
        altura = request.POST.get("altura")
        objetivo = request.POST.get("objetivo")
        notas = request.POST.get("notas")

        Cliente.objects.create(
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            edad=edad or None,
            peso=peso or None,
            altura=altura or None,
            objetivo=objetivo,
            notas=notas
        )

        return redirect("/clientes/")

    return render(
        request,
        "core/agregar_cliente.html"
    )


# ==========================================
# VER CLIENTE
# ==========================================

@login_required
@user_passes_test(es_administrador)
def ver_cliente(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id
    )

    rutinas = cliente.rutinas.all()

    progresos = cliente.progresos.all().order_by("-fecha")

    return render(
        request,
        "core/ver_cliente.html",
        {
            "cliente": cliente,
            "rutinas": rutinas,
            "progresos": progresos,
        }
    )


# ==========================================
# CREAR RUTINA
# ==========================================

@login_required
@user_passes_test(es_administrador)
def agregar_rutina(request, cliente_id):

    cliente = get_object_or_404(
        Cliente,
        id=cliente_id
    )

    if request.method == "POST":

        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")

        Rutina.objects.create(
            nombre=nombre,
            cliente=cliente,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio or None,
            activa=True
        )

        return redirect(
            f"/clientes/{cliente.id}/"
        )

    return render(
        request,
        "core/agregar_rutina.html",
        {
            "cliente": cliente
        }
    )


# ==========================================
# AGREGAR EJERCICIO A UNA RUTINA
# ==========================================

@login_required
@user_passes_test(es_administrador)
def agregar_ejercicio_rutina(request, rutina_id):

    rutina = get_object_or_404(
        Rutina,
        id=rutina_id
    )

    ejercicios = Ejercicio.objects.all().order_by("nombre")

    if request.method == "POST":

        ejercicio_id = request.POST.get("ejercicio")
        series = request.POST.get("series")
        repeticiones = request.POST.get("repeticiones")
        peso = request.POST.get("peso")
        descanso = request.POST.get("descanso")
        orden = request.POST.get("orden")

        ejercicio = get_object_or_404(
            Ejercicio,
            id=ejercicio_id
        )

        EjercicioRutina.objects.create(
            rutina=rutina,
            ejercicio=ejercicio,
            series=series or 3,
            repeticiones=repeticiones or 10,
            peso=peso or None,
            descanso=descanso or 60,
            orden=orden or 1
        )

        return redirect(
            f"/rutinas/{rutina.id}/ejercicio/agregar/"
        )

    ejercicios_rutina = rutina.ejercicios_rutina.all().order_by("orden")

    return render(
        request,
        "core/agregar_ejercicio_rutina.html",
        {
            "rutina": rutina,
            "ejercicios": ejercicios,
            "ejercicios_rutina": ejercicios_rutina,
        }
    )


# ==========================================
# LOGIN
# ==========================================

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

            return redirect("/")

        mensaje = "Usuario o contraseña incorrectos."

    return render(
        request,
        "core/login.html",
        {
            "mensaje": mensaje
        }
    )