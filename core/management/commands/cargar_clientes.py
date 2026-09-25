from django.core.management.base import BaseCommand
from core.models import Cliente


class Command(BaseCommand):
    help = "Carga los clientes iniciales de FitnessApp"

    def handle(self, *args, **options):

        clientes = [
            {
                "nombre": "Juan Pérez",
                "correo": "familiarojasmendez3@gmail.com",
                "telefono": "8888-8888",
            },
            {
                "nombre": "Carlos Fitness",
                "correo": "carlos@fitness.com",
                "telefono": "88888888",
            },
            {
                "nombre": "María Fitness",
                "correo": "maria@fitness.com",
                "telefono": "88887777",
            },
        ]

        for datos in clientes:

            cliente, creado = Cliente.objects.get_or_create(
                correo=datos["correo"],
                defaults={
                    "nombre": datos["nombre"],
                    "telefono": datos["telefono"],
                },
            )

            if creado:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Cliente creado: {cliente.nombre}"
                    )
                )
            else:
                self.stdout.write(
                    f"Cliente ya existía: {cliente.nombre}"
                )

        self.stdout.write(
            self.style.SUCCESS("Proceso terminado correctamente.")
        )
