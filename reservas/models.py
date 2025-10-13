from django.db import models
from django.contrib.auth.models import User 
from servicios.models import Servicio
from django.urls import reverse

class Barbero(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="barbero")
    especialidad = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='barberos/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Barbero"
        verbose_name_plural = "Barberos"
        ordering = ['usuario__first_name']
    
    def __str__(self):
        return f"{self.usuario.get_full_name()}"
    
    def get_absolute_url(self):
        return reverse('horarios_barbero', kwargs={'barbero_id': self.id})
    
    @property
    def nombre_completo(self):
        return self.usuario.get_full_name()
    
    @property
    def foto_url(self):
        """Devuelve la URL de la foto o una por defecto"""
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/images/barbero-default.png'  # Crea esta imagen en tu static

class Disponibilidad(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE, related_name="disponibilidades")
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)

    class Meta:
        unique_together = ['barbero', 'fecha', 'hora']
        ordering = ['fecha', 'hora']

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"{self.barbero} - {self.fecha} {self.hora.strftime('%H:%M')} ({estado})"
class Cita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="citas")
    disponibilidad = models.OneToOneField(Disponibilidad, on_delete=models.CASCADE, related_name="cita")
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True)
    duracion_servicio = models.PositiveIntegerField(default=30)  # 🔹 nuevo
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-disponibilidad__fecha', '-disponibilidad__hora']

    def __str__(self):
        return f"{self.cliente.username} - {self.disponibilidad.fecha} {self.disponibilidad.hora}"
