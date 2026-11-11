from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import OperationalError, ProgrammingError
from usuarios.demo_seed import seed_demo


class Command(BaseCommand):
    help = 'Adiciona dados fictícios aos perfis existentes, sem apagar registros ou duplicar o seed.'

    def handle(self, *args, **options):
        if settings.READ_ONLY_DEMO:
            raise CommandError('Seed desativado no runtime somente leitura. O build gera seu próprio banco fictício.')
        try:
            counts = seed_demo()
        except (ValueError, OperationalError, ProgrammingError) as exc:
            raise CommandError(f'Seed não aplicado (transação revertida). Confira as migrações: {exc}') from exc
        self.stdout.write(self.style.SUCCESS('Registros criados: ' + ', '.join(f'{key}={value}' for key, value in counts.items())))
