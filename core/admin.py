from django.contrib import admin
from .models import Cliente, Ejercicio, Rutina, EjercicioRutina, Progreso


class EjercicioRutinaInline(admin.TabularInline):
    model = EjercicioRutina
    extra = 1


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "cliente", "fecha_inicio", "activa")
    list_filter = ("activa", "fecha_inicio")
    search_fields = ("nombre", "cliente__nombre")
    inlines = [EjercicioRutinaInline]


@admin.register(Progreso)
class ProgresoAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "fecha",
        "peso",
        "repeticiones",
        "peso_ejercicio",
    )

    list_filter = ("fecha",)

    search_fields = (
        "cliente__nombre",
    )


admin.site.register(Cliente)
admin.site.register(Ejercicio)