from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea superusuarios admin y angello si no existen'

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
