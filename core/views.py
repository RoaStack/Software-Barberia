from django.shortcuts import render
from servicios.models import Servicio

def home(request):
    servicios = Servicio.objects.all()
    return render(request, 'core/home.html', {'servicios': servicios})
