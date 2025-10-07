from django import forms
from .models import Disponibilidad

class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = Disponibilidad
        fields = ["fecha", "hora", "disponible"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }
