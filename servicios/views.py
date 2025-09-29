from django.shortcuts import render, get_object_or_404
from .models import Servicio

def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/lista.html', {'servicios': servicios})

def detalle_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    return render(request, 'servicios/detalle.html', {'servicio': servicio})
