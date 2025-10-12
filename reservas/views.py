from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Disponibilidad, Cita, Servicio
from reservas.models import Barbero 
from django.utils import timezone
from .forms import DisponibilidadForm 
from django.db import transaction
from .emails import enviar_correo_reserva, enviar_correo_confirmacion, enviar_correo_cancelacion
from datetime import date


# ---------------------------
# CLIENTE y BARBERO COMPARTEN
# ---------------------------

@login_required
def disponibilidades(request):
    """
    Muestra las disponibilidades:
    - Si es Barbero: solo las suyas (puede crear nuevas)
    - Si es Cliente: todas las disponibles para reservar
    """
    if request.user.groups.filter(name="Barbero").exists():
        # Barbero: ver y crear sus horarios
        barbero = get_object_or_404(Barbero, usuario=request.user)
        disponibilidades = Disponibilidad.objects.filter(barbero=barbero).order_by("fecha", "hora")

        # --- Crear nueva disponibilidad ---
        if request.method == "POST":
            fecha = request.POST.get("fecha")
            hora = request.POST.get("hora")

            # Validaciones básicas
            if not fecha or not hora:
                messages.error(request, "Debes ingresar una fecha y hora.")
            else:
                # Evitar duplicados
                existe = Disponibilidad.objects.filter(barbero=barbero, fecha=fecha, hora=hora).exists()
                if existe:
                    messages.warning(request, "Ya tienes un horario creado en esa fecha y hora.")
                else:
                    Disponibilidad.objects.create(barbero=barbero, fecha=fecha, hora=hora, disponible=True)
                    messages.success(request, "Disponibilidad agregada correctamente.")
                    return redirect("reservas:disponibilidades")

        return render(request, "reservas/disponibilidades_barbero.html", {"disponibilidades": disponibilidades})

    else:
        # Cliente: ver horarios disponibles para reserva
        disponibilidades = Disponibilidad.objects.filter(disponible=True).order_by("fecha", "hora")
        return render(request, "reservas/disponibilidades.html", {"disponibilidades": disponibilidades})


@login_required
def reservar(request, disponibilidad_id):
    """Permite a un cliente reservar una cita de forma segura."""
    with transaction.atomic():
        disponibilidad = Disponibilidad.objects.select_for_update().get(id=disponibilidad_id, disponible=True)
        
        if request.method == "POST":
            servicio_id = request.POST.get("servicio")
            servicio = get_object_or_404(Servicio, id=servicio_id)

            # Crear la cita con duración del servicio
            cita = Cita.objects.create(
                cliente=request.user,
                disponibilidad=disponibilidad,
                servicio=servicio,
                duracion_servicio=servicio.duracion,
            )

            # Marcar disponibilidad como ocupada
            disponibilidad.disponible = False
            disponibilidad.save()

            # ✉️ Enviar correo de reserva (HTML) - CORREGIDO
            enviar_correo_reserva(cita)

            messages.success(request, "Tu cita fue reservada con éxito.")
            return redirect("reservas:mis_reservas")

        servicios = Servicio.objects.all()
        return render(request, "reservas/reservar.html", {
            "disponibilidad": disponibilidad,
            "servicios": servicios
        })


@login_required
def mis_reservas(request):
    """Muestra las reservas del cliente o barbero."""
    if request.user.groups.filter(name="Barbero").exists():
        citas = Cita.objects.filter(disponibilidad__barbero__usuario=request.user).order_by("disponibilidad__fecha", "disponibilidad__hora")
        return render(request, "reservas/mis_reservas_barbero.html", {"citas": citas})
    else:
        citas = Cita.objects.filter(cliente=request.user).order_by("-disponibilidad__fecha", "-disponibilidad__hora")
        return render(request, "reservas/mis_reservas.html", {"citas": citas})


@login_required
def cancelar_reserva(request, cita_id):
    """Permite a un cliente cancelar una cita pendiente."""
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user, estado="pendiente")
    cita.estado = "cancelada"
    cita.disponibilidad.disponible = True
    cita.disponibilidad.save()
    cita.save()

    # ✉️ Enviar correo de cancelación (HTML) - CORREGIDO
    enviar_correo_cancelacion(cita)

    messages.success(request, "La reserva fue cancelada.")
    return redirect("reservas:mis_reservas")


@login_required
def confirmar_reserva(request, cita_id):
    """Permite al barbero confirmar una cita."""
    cita = get_object_or_404(Cita, id=cita_id, disponibilidad__barbero__usuario=request.user, estado="pendiente")
    cita.estado = "confirmada"
    cita.save()

    # ✉️ Enviar correo de confirmación (HTML) - CORREGIDO
    enviar_correo_confirmacion(cita)

    messages.success(request, "La reserva fue confirmada.")
    return redirect("reservas:mis_reservas")


# ---------------------------
# DASHBOARD DEL BARBERO
# ---------------------------

@login_required
def dashboard_barbero(request):
    """Panel del barbero con métricas y citas."""
    if not request.user.groups.filter(name="Barbero").exists():
        messages.error(request, "No tienes permiso para acceder a este panel.")
        return redirect("reservas:mis_reservas")

    citas = Cita.objects.filter(disponibilidad__barbero__usuario=request.user).order_by("disponibilidad__fecha", "disponibilidad__hora")
    disponibilidades = Disponibilidad.objects.filter(barbero__usuario=request.user).order_by("fecha", "hora")

    contexto = {
        "citas": citas,
        "disponibilidades": disponibilidades,
        "total_citas": citas.count(),
        "pendientes": citas.filter(estado="pendiente").count(),
        "confirmadas": citas.filter(estado="confirmada").count(),
        "completadas": citas.filter(estado="completada").count(),
    }

    return render(request, "reservas/dashboard_barbero.html", contexto)


# ---------------------------
# DISPONIBILIDAD MÚLTIPLE
# ---------------------------

@login_required
def gestionar_disponibilidad(request):
    """Permite al barbero crear varias horas para una misma fecha."""
    if not request.user.groups.filter(name="Barbero").exists():
        messages.error(request, "No tienes permiso para gestionar disponibilidades.")
        return redirect("reservas:mis_reservas")

    barbero = Barbero.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = DisponibilidadForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            horas = form.cleaned_data['horas']

            creadas = 0
            for h in horas:
                obj, created = Disponibilidad.objects.get_or_create(
                    barbero=barbero,
                    fecha=fecha,
                    hora=h,
                    defaults={'disponible': True}
                )
                if created:
                    creadas += 1

            messages.success(request, f"{creadas} horas agregadas correctamente para {fecha}.")
            return redirect('reservas:gestionar_disponibilidad')
    else:
        form = DisponibilidadForm()

    disponibilidades = Disponibilidad.objects.filter(barbero=barbero).order_by('-fecha', 'hora')
    return render(request, 'reservas/gestionar_disponibilidad.html', {
        'form': form,
        'disponibilidades': disponibilidades
    })


@login_required
def eliminar_disponibilidad(request, disponibilidad_id):
    """Permite al barbero eliminar sus propias disponibilidades."""
    disponibilidad = get_object_or_404(Disponibilidad, id=disponibilidad_id, barbero__usuario=request.user)
    disponibilidad.delete()
    messages.success(request, "Disponibilidad eliminada correctamente.")
    return redirect("reservas:gestionar_disponibilidad")

@login_required
def lista_barberos(request):
    barberos = Barbero.objects.all()
    return render(request, "reservas/lista_barberos.html", {"barberos": barberos})

@login_required
def horarios_barbero(request, barbero_id):
    barbero = get_object_or_404(Barbero, id=barbero_id)
    fecha_seleccionada = request.GET.get("fecha", date.today())

    horarios_disponibles = Disponibilidad.objects.filter(
        barbero=barbero,
        fecha=fecha_seleccionada,
        disponible=True
    ).order_by("hora")

    context = {
        "barbero": barbero,
        "fecha": fecha_seleccionada,
        "horarios_disponibles": horarios_disponibles,
    }
    return render(request, "reservas/horarios_disponibles.html", context)