import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission


class Command(BaseCommand):
    """
    Crea (si no existen) el grupo 'Operador' con permiso de solo lectura
    sobre clientes, y un usuario demo asignado a ese grupo. Pensado para
    correr en cada deploy sin duplicar datos ni fallar si ya existen.

    Requiere las variables de entorno:
    - DEMO_USER_USERNAME
    - DEMO_USER_PASSWORD
    """
    help = 'Crea el grupo Operador (solo lectura) y un usuario demo asignado a él'

    def handle(self, *args, **options):
        # Paso 1 — Crear el grupo Operador si no existe, con permiso view_client
        group, created = Group.objects.get_or_create(name='Operador')
        if created:
            try:
                perm = Permission.objects.get(codename='view_client')
                group.permissions.set([perm])
                self.stdout.write(self.style.SUCCESS('✅ Grupo "Operador" creado con permiso view_client.'))
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING('⚠️  Permiso "view_client" no encontrado todavía.'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Grupo "Operador" ya existía, no se modifica.'))

        # Paso 2 — Crear el usuario demo si no existe
        username = os.environ.get('DEMO_USER_USERNAME')
        password = os.environ.get('DEMO_USER_PASSWORD')

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  DEMO_USER_USERNAME o DEMO_USER_PASSWORD no están definidas. Se omite la creación.'
                )
            )
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'✅ El usuario demo "{username}" ya existe, no se crea de nuevo.'))
            return

        user = User.objects.create_user(username=username, password=password)
        user.groups.set([group])
        user.save()
        self.stdout.write(self.style.SUCCESS(f'✅ Usuario demo "{username}" creado y asignado a "Operador".'))
