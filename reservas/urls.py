# reservas/urls.py
from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("disponibilidades/", views.disponibilidades, name="disponibilidades"),
    path("reservar/<int:disponibilidad_id>/", views.reservar, name="reservar"),
    path("mis_reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:cita_id>/", views.cancelar_reserva, name="cancelar_reserva"),
    path("confirmar/<int:cita_id>/", views.confirmar_reserva, name="confirmar_reserva"),
    path("dashboard_barbero/", views.dashboard_barbero, name="dashboard_barbero"),
    path("gestionar_disponibilidad/", views.gestionar_disponibilidad, name="gestionar_disponibilidad"),
    path("eliminar_disponibilidad/<int:disponibilidad_id>/", views.eliminar_disponibilidad, name="eliminar_disponibilidad"),
]
