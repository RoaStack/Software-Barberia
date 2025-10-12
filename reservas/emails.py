from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def enviar_correo_html(asunto, template, contexto, destinatarios):
    """Función genérica para enviar correos HTML."""
    html_content = render_to_string(template, contexto)
    text_content = (
        f"{asunto}\n\nPor favor, visualiza este correo en formato HTML para ver los detalles correctamente."
    )

    email = EmailMultiAlternatives(asunto, text_content, settings.DEFAULT_FROM_EMAIL, destinatarios)
    email.attach_alternative(html_content, "text/html")
    email.send()

# -----------------------------
# CORREOS ESPECÍFICOS
# -----------------------------

def enviar_correo_reserva(cita):
    asunto = "💈 Nueva reserva generada"
    contexto = {"cita": cita}
    destinatarios = [cita.cliente.email, cita.disponibilidad.barbero.usuario.email]
    enviar_correo_html(asunto, "emails/reserva_creada.html", contexto, destinatarios)

def enviar_correo_confirmacion(cita):
    asunto = "✅ Tu cita ha sido confirmada"
    contexto = {"cita": cita}
    destinatarios = [cita.cliente.email]
    enviar_correo_html(asunto, "emails/reserva_confirmada.html", contexto, destinatarios)

def enviar_correo_cancelacion(cita):
    asunto = "❌ Cita cancelada"
    contexto = {"cita": cita}
    destinatarios = [cita.cliente.email, cita.disponibilidad.barbero.usuario.email]
    enviar_correo_html(asunto, "emails/reserva_cancelada.html", contexto, destinatarios)
