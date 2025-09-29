from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disponibilidad, Cita, Servicio

@login_required
def disponibilidades(request):
    disponibilidades = Disponibilidad.objects.filter(disponible=True).order_by("fecha", "hora")
    return render(request, "reservas/disponibilidades.html", {"disponibilidades": disponibilidades})

@login_required
def reservar(request, disponibilidad_id):
    disponibilidad = get_object_or_404(Disponibilidad, id=disponibilidad_id, disponible=True)
    if request.method == "POST":
        servicio_id = request.POST.get("servicio")
        servicio = get_object_or_404(Servicio, id=servicio_id)
        cita = Cita.objects.create(cliente=request.user, disponibilidad=disponibilidad, servicio=servicio)
        disponibilidad.disponible = False
        disponibilidad.save()
        messages.success(request, "Tu cita fue reservada con éxito.")
        return redirect("reservas:mis_reservas")
    servicios = Servicio.objects.all()
    return render(request, "reservas/reservar.html", {"disponibilidad": disponibilidad, "servicios": servicios})

@login_required
def mis_reservas(request):
    if request.user.groups.filter(name="Barbero").exists():
        citas = Cita.objects.filter(disponibilidad__barbero__usuario=request.user)
    else:
        citas = Cita.objects.filter(cliente=request.user)
    return render(request, "reservas/mis_reservas.html", {"citas": citas})

@login_required
def cancelar_reserva(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user, estado="pendiente")
    cita.estado = "cancelada"
    cita.disponibilidad.disponible = True
    cita.disponibilidad.save()
    cita.save()
    messages.success(request, "La reserva fue cancelada.")
    return redirect("reservas:mis_reservas")

@login_required
def confirmar_reserva(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, disponibilidad__barbero__usuario=request.user, estado="pendiente")
    cita.estado = "confirmada"
    cita.save()
    messages.success(request, "La reserva fue confirmada.")
    return redirect("reservas:mis_reservas")
