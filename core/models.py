from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cliente"
    )

    nombre = models.CharField(max_length=100)

    correo = models.EmailField(
        unique=True
    )

    telefono = models.CharField(
        max_length=20,
        blank=True
    )

    edad = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    altura = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    objetivo = models.CharField(
        max_length=200,
        blank=True
    )

    notas = models.TextField(
        blank=True
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    descripcion = models.TextField(
        blank=True
    )

    grupo_muscular = models.CharField(
        max_length=100
    )

    instrucciones = models.TextField(
        blank=True
    )

    imagen = models.URLField(
        blank=True
    )

    video = models.URLField(
        blank=True
    )

    def __str__(self):
        return self.nombre


class Rutina(models.Model):

    nombre = models.CharField(
        max_length=150
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="rutinas"
    )

    descripcion = models.TextField(
        blank=True
    )

    fecha_inicio = models.DateField(
        null=True,
        blank=True
    )

    activa = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.cliente.nombre}"


class EjercicioRutina(models.Model):

    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name="ejercicios_rutina"
    )

    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE,
        related_name="rutinas"
    )

    series = models.PositiveIntegerField(
        default=3
    )

    repeticiones = models.PositiveIntegerField(
        default=10
    )

    peso = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    descanso = models.PositiveIntegerField(
        default=60,
        help_text="Descanso en segundos"
    )

    orden = models.PositiveIntegerField(
        default=1
    )

    completado = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.rutina.nombre} - {self.ejercicio.nombre}"


class Progreso(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="progresos"
    )

    fecha = models.DateField(
        auto_now_add=True
    )

    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    repeticiones = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    peso_ejercicio = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )

    notas = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.cliente.nombre} - {self.fecha}"