import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Crea el usuario administrador de FitnessApp si no existe"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD")

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    "ADMIN_PASSWORD no está configurada."
                )
            )
            return

        usuario, creado = User.objects.get_or_create(
            username=username
        )

        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.set_password(password)
        usuario.save()

        if creado:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuario administrador '{username}' creado correctamente."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Usuario administrador '{username}' actualizado correctamente."
                )
            )