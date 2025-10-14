from django.db import models
from django.contrib.auth.models import User 
from servicios.models import Servicio
from django.urls import reverse
from cloudinary.models import CloudinaryField

class Barbero(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="barbero")
    especialidad = models.CharField(max_length=100, blank=True)
    foto = CloudinaryField('foto', folder='barberos/',null=True,blank=True)
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
        if self.foto:
            return self.foto.url
        return '/static/images/logoBarberia.png'


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
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.CASCADE, related_name="citas")  # CAMBIADO: OneToOne → ForeignKey
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True)
    duracion_servicio = models.PositiveIntegerField(default=30)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-disponibilidad__fecha', '-disponibilidad__hora']
        # Agrega esta constraint para evitar reservas duplicadas activas
        constraints = [
            models.UniqueConstraint(
                fields=['disponibilidad'], 
                condition=models.Q(estado__in=['pendiente', 'confirmada']),
                name='unique_disponibilidad_activa'
            )
        ]

    def __str__(self):
        return f"{self.cliente.username} - {self.disponibilidad.fecha} {self.disponibilidad.hora} ({self.estado})"
