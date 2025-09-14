from django.db import models
from decimal import Decimal

"""
• Cliente: nombre, apellido, teléfono, email (opcional).
• Vehiculo: patente (única), marca, modelo, año, relacionado a un Cliente.
• Servicio: nombre (único), precio.
• OrdenReparacion: vehículo (FK), servicios (Muchos a Muchos), fecha_ingreso, fecha_salida (opcional),
estado (ingresado, en_progreso, finalizado), monto_total.

"""

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'Nombre Completo: {self.nombre} {self.apellido}\n'



class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=30)
    año = models.PositiveIntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vehiculos")

    def __str__(self):
        return (
        f"Descripción:\n"
        f"  Patente: {self.patente}\n"
        f"  Marca: {self.marca}\n"
        f"  Modelo: {self.modelo}\n"
        f"  Año: {self.año}\n"
    )


class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=500, default="Sin Descripción")

    def __str__(self):
        return f'{self.nombre} - ${self.precio}\n'



class ordenReparacion(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='ordenReparacion')
    servicios = models.ManyToManyField(Servicio, related_name='ordenes')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(choices=[('ingresado', 'Ingresado'),('en_progreso','En Progreso'),('finalizado', 'Finalizado')], default='ingresado')
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def calcularTotal(self):
        total = Decimal(0)
        
        for servicio in self.servicios.all():
            total += servicio.precio
        
        self.monto_total = total
        self.save()
        return total