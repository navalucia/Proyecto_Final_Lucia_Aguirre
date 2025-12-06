from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tienda.models import AdminPersonalizado

class Command(BaseCommand):
    help = 'Crea un usuario administrador personalizado'

    def handle(self, *args, **options):
        username = 'admin_skincare'
        email = 'admin@skincareshop.com'
        password = 'admin123'
        
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=False
            )
            
            # Crear el administrador personalizado
            AdminPersonalizado.objects.create(usuario=user)
            
            self.stdout.write(
                self.style.SUCCESS(f'Administrador "{username}" creado exitosamente')
            )
            self.stdout.write(
                self.style.WARNING(f'Credenciales: Usuario: {username} | Contraseña: {password}')
            )
        else:
            user = User.objects.get(username=username)
            # Asegurarse de que exista el AdminPersonalizado
            AdminPersonalizado.objects.get_or_create(usuario=user)
            self.stdout.write(
                self.style.WARNING(f'El administrador "{username}" ya existe')
            )