from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    """
    Comando personalizado para asignar un rol a un usuario.
    Uso: python manage.py asignar_rol <username> <rol>
    Ejemplo: python manage.py asignar_rol elvisdga Administrador
    """

    help = 'Asigna un usuario a un grupo (rol) del sistema'

    def add_arguments(self, parser):
        """
        Define los argumentos que recibe el comando.
        - username: el nombre del usuario a modificar
        - rol: el nombre del grupo a asignar (Administrador u Operador)
        """
        parser.add_argument(
            'username',
            type=str,
            help='Nombre de usuario al que se le asignará el rol'
        )
        parser.add_argument(
            'rol',
            type=str,
            help='Nombre del rol a asignar: Administrador u Operador'
        )

    def handle(self, *args, **options):
        """
        Lógica principal del comando.
        Se ejecuta cuando llamas: python manage.py asignar_rol
        """
        username = options['username']
        rol = options['rol']

        # Paso 1 — Buscar el usuario
        try:
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: El usuario "{username}" no existe')
            )
            return

        # Paso 2 — Buscar el grupo
        try:
            grupo = Group.objects.get(name=rol)
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: El rol "{rol}" no existe. Usa: Administrador u Operador')
            )
            return

        # Paso 3 — Asignar el usuario al grupo
        usuario.groups.set([grupo])

        # Paso 4 — Confirmar
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Usuario "{username}" asignado correctamente al rol "{rol}"'
            )
        )
