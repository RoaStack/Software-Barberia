from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    duracion = models.PositiveIntegerField(default=30, help_text="Duración del servicio en minutos")  # 🔹 nuevo

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
