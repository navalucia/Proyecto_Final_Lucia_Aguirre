# tienda/management/commands/cargar_datos_iniciales.py

from django.core.management.base import BaseCommand
from tienda.models import Categoria

class Command(BaseCommand):
    help = 'Carga datos iniciales para la tienda'

    def handle(self, *args, **options):
        categorias = [
            'Hidratantes',
            'Antiedad', 
            'Acné',
            'Sensibles',
            'Normales',
            'Secas',
            'Grasas',
            'Mixtas'
        ]
        
        for nombre in categorias:
            Categoria.objects.get_or_create(nombre=nombre)
        
        self.stdout.write(
            self.style.SUCCESS('Datos iniciales cargados exitosamente')
        )