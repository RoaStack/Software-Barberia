from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def enviar_correo_html(asunto, template, contexto, destinatarios):
    """Función genérica para enviar correos HTML."""
    html_content = render_to_string(template, contexto)
    text_content = f"{asunto}\n\nPor favor, visualiza este correo en formato HTML."

    try:
        msg = EmailMultiAlternatives(
            subject=asunto,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=destinatarios
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.error(f"❌ Error al enviar correo: {e}")
        # También puedes imprimir para ver en logs de Render
        print(f"❌ Error al enviar correo: {e}")

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
