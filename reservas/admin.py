from django.contrib import admin
from django.utils.html import format_html
from .models import Barbero, Disponibilidad, Cita

class BarberoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'foto_preview', 'activo']
    list_filter = ['activo', 'especialidad']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidad']
    list_editable = ['activo']
    
    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.foto.url)
        return "Sin foto"
    foto_preview.short_description = 'Foto'

admin.site.register(Barbero, BarberoAdmin)
admin.site.register(Disponibilidad)
admin.site.register(Cita)