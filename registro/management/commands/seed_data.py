from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from registro.models import Evento


class Command(BaseCommand):
    help = 'Crea superusuario admin y evento de prueba si no existen'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@backstage.com', 'admin1234')
            self.stdout.write(self.style.SUCCESS('Superusuario admin creado'))
        else:
            self.stdout.write('Superusuario admin ya existe')

        if not User.objects.filter(username='angello').exists():
            User.objects.create_superuser('angello', 'angello@backstage.com', 'Backstage2026')
            self.stdout.write(self.style.SUCCESS('Superusuario angello creado'))
        else:
            self.stdout.write('Superusuario angello ya existe')

        if not Evento.objects.filter(slug='stage-lab').exists():
            Evento.objects.create(
                nombre='Stage Lab · Laboratorio de Escena',
                descripcion='Ciclo intensivo de creacion musical',
                fecha=timezone.now(),
                lugar='Lima Peru',
                slug='stage-lab',
                activo=True,
            )
            self.stdout.write(self.style.SUCCESS('Evento stage-lab creado'))
        else:
            self.stdout.write('Evento stage-lab ya existe')
