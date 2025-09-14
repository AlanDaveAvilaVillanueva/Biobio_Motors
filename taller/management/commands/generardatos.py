from django.core.management.base import BaseCommand
from faker import Faker
from taller.models import Cliente, Vehiculo, Servicio, ordenReparacion  # ajusta "taller" al nombre de tu app
import random
from decimal import Decimal


class Command(BaseCommand):
    help = "Genera datos ficticios para pruebas"

    def handle(self, *args, **options):
        fake = Faker("es_ES")

        # Limpiar datos anteriores (opcional)
        Cliente.objects.all().delete()
        Vehiculo.objects.all().delete()
        Servicio.objects.all().delete()
        ordenReparacion.objects.all().delete()

         # Crear 2 clientes
        clientes = []
        for _ in range(2):
            c = Cliente.objects.create(
                nombre=fake.first_name(),
                apellido=fake.last_name(),
                telefono=fake.phone_number(),
                email=fake.email()
            )
            clientes.append(c)

        # Crear 1 vehículo para cada cliente
        vehiculos = []
        for cliente in clientes:
            v = Vehiculo.objects.create(
                patente=fake.license_plate(),
                marca=fake.company(),
                modelo=fake.word().capitalize(),
                año=random.randint(2000, 2023),
                cliente=cliente
            )
            vehiculos.append(v)

        # Crear 3 servicios distintos
        servicios = []
        for _ in range(3):
            s = Servicio.objects.create(
                nombre=fake.word().capitalize(),
                precio=Decimal(random.randint(10000, 50000)),
                descripcion=fake.sentence(nb_words=6)
            )
            servicios.append(s)

        # Crear 2 órdenes de reparación con 1 o más servicios asociados
        for vehiculo in vehiculos[:2]:  # 2 órdenes, un vehículo por orden
            orden = ordenReparacion.objects.create(
                vehiculo=vehiculo,
                estado=random.choice(['ingresado', 'en_progreso', 'finalizado']),
                monto_total=0
            )
            servicios_seleccionados = random.sample(servicios, k=random.randint(1, 3))
            orden.servicios.set(servicios_seleccionados)
            orden.calcularTotal()

        self.stdout.write(self.style.SUCCESS("✅ Datos de prueba con Faker creados con éxito"))
