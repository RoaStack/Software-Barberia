from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    # === NUEVO FLUJO DE RESERVA POR BARBERO ===
    path("barberos/", views.lista_barberos, name="lista_barberos"),
    path("barberos/<int:barbero_id>/horarios/", views.horarios_barbero, name="horarios_barbero"),

    # === EXISTENTES (se mantienen) ===
    path("disponibilidades/", views.disponibilidades, name="disponibilidades"),
    path("reservar/<int:disponibilidad_id>/", views.reservar, name="reservar"),
    path("mis_reservas/", views.mis_reservas, name="mis_reservas"),
    path("cancelar/<int:cita_id>/", views.cancelar_reserva, name="cancelar_reserva"),
    path("confirmar/<int:cita_id>/", views.confirmar_reserva, name="confirmar_reserva"),
    
    # === NUEVA URL PARA CANCELAR RESERVA DESDE BARBERO ===
    path("cancelar-barbero/<int:cita_id>/", views.cancelar_reserva_barbero, name="cancelar_reserva_barbero"),

    # === FUNCIONALIDADES DEL BARBERO ===
    path("dashboard_barbero/", views.dashboard_barbero, name="dashboard_barbero"),
    path("gestionar_disponibilidad/", views.gestionar_disponibilidad, name="gestionar_disponibilidad"),
    path("eliminar_disponibilidad/<int:disponibilidad_id>/", views.eliminar_disponibilidad, name="eliminar_disponibilidad"),
]