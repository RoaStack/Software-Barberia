from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ Asignar automáticamente al grupo Cliente
            grupo_cliente, _ = Group.objects.get_or_create(name="Cliente")
            user.groups.add(grupo_cliente)

            login(request, user)
            return redirect("usuarios:dashboard")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def dashboard(request):
    # ✅ Detecta si el usuario es barbero o cliente
    if request.user.groups.filter(name="Barbero").exists():
        return render(request, "usuarios/dashboard_barbero.html")
    return render(request, "usuarios/dashboard_cliente.html")
