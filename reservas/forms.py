from datetime import time
from django import forms
from .models import Disponibilidad

# Rango de horas de trabajo (puedes ajustarlo libremente)
HORAS_OPCIONES = [
    (time(h, 0), f"{h:02d}:00") for h in range(9, 21)
]

class DisponibilidadForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.SelectDateWidget,
        label="Fecha de disponibilidad"
    )
    horas = forms.MultipleChoiceField(
        choices=HORAS_OPCIONES,
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona las horas disponibles"
    )
