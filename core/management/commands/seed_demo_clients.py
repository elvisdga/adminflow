from django.core.management.base import BaseCommand
from core.models import Client


class Command(BaseCommand):
    """
    Carga un set de clientes de ejemplo para la demo, si todavía no existen.
    Usa el email como identificador único para no duplicar registros
    en cada redeploy.
    """
    help = 'Crea clientes de ejemplo para la demo en vivo, si no existen'

    DEMO_CLIENTS = [
        {"name": "Laura Méndez", "email": "lmendez@construnorte.com", "phone": "5551234567"},
        {"name": "Roberto Salinas", "email": "rsalinas@textilesdelvalle.com", "phone": "5559876543"},
        {"name": "Patricia Vega", "email": "pvega@logisticaandina.com", "phone": "5554567890"},
        {"name": "Fernando Castillo", "email": "fcastillo@agroexport.com", "phone": "5553216549"},
        {"name": "Sandra Ortiz", "email": "sortiz@clinicasanmiguel.com", "phone": "5557894561"},
    ]

    def handle(self, *args, **options):
        creados = 0
        for data in self.DEMO_CLIENTS:
            _, created = Client.objects.get_or_create(
                email=data["email"],
                defaults={"name": data["name"], "phone": data["phone"]},
            )
            if created:
                creados += 1

        if creados:
            self.stdout.write(self.style.SUCCESS(f'✅ {creados} clientes de ejemplo creados.'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ Los clientes de ejemplo ya existían, no se duplicaron.'))
