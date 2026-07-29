import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Crea un superusuario automáticamente a partir de variables de entorno,
    si todavía no existe. Pensado para correr en cada deploy sin duplicar
    usuarios ni fallar si ya fue creado antes.

    Requiere las variables de entorno:
    - DJANGO_SUPERUSER_USERNAME
    - DJANGO_SUPERUSER_EMAIL
    - DJANGO_SUPERUSER_PASSWORD
    """
    help = 'Crea un superusuario desde variables de entorno si no existe'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  DJANGO_SUPERUSER_USERNAME o DJANGO_SUPERUSER_PASSWORD '
                    'no están definidas. Se omite la creación.'
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'✅ El superusuario "{username}" ya existe, no se crea de nuevo.')
            )
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Superusuario "{username}" creado correctamente.')
        )
