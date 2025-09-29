from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("disponibilidades/", views.disponibilidades, name="disponibilidades"),
    path("reservar/<int:disponibilidad_id>/", views.reservar, name="reservar"),
    path("mis-reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:cita_id>/", views.cancelar_reserva, name="cancelar"),
    path("confirmar/<int:cita_id>/", views.confirmar_reserva, name="confirmar"),
]
