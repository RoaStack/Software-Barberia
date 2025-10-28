from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from reservas.models import Cita
from .forms import RegistroForm
from datetime import date
from django.db.models import Min

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo_cliente, _ = Group.objects.get_or_create(name="Cliente")
            user.groups.add(grupo_cliente)
            login(request, user)
            messages.success(request, "¡Tu cuenta fue creada con éxito! 🎉")
            return redirect("usuarios:dashboard")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def dashboard(request):
    # ✅ Si es barbero
    if request.user.groups.filter(name="Barbero").exists():
        citas = Cita.objects.filter(disponibilidad__barbero__usuario=request.user)

        # ✅ Conteos por estado
        total_citas = citas.count()
        pendientes = citas.filter(estado="pendiente").count()
        confirmadas = citas.filter(estado="confirmada").count()
        completadas = citas.filter(estado="completada").count()

        # ✅ Fecha actual
        hoy = date.today()

        # 🔹 Primero buscamos citas para hoy
        citas_hoy = citas.filter(disponibilidad__fecha=hoy).order_by("disponibilidad__hora")

        if citas_hoy.exists():
            citas_proximas = citas_hoy
        else:
            # 🔹 Si no hay hoy, buscamos la próxima fecha más cercana con citas
            proxima_fecha = citas.filter(disponibilidad__fecha__gt=hoy)\
                                 .aggregate(proxima=Min("disponibilidad__fecha"))["proxima"]

            if proxima_fecha:
                citas_proximas = citas.filter(disponibilidad__fecha=proxima_fecha)\
                                      .order_by("disponibilidad__hora")
            else:
                citas_proximas = Cita.objects.none()

        contexto = {
            "total_citas": total_citas,
            "pendientes": pendientes,
            "confirmadas": confirmadas,
            "completadas": completadas,
            "citas": citas_proximas[:5],  # solo las primeras 5 del día encontrado
        }

        return render(request, "usuarios/dashboard_barbero.html", contexto)

    # ✅ Si es cliente
    return render(request, "usuarios/dashboard_cliente.html")
