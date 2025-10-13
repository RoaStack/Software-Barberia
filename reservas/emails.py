from django.template.loader import render_to_string
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_correo_html(asunto, template, contexto, destinatarios):
    html_content = render_to_string(template, contexto)
    message = Mail(
        from_email=os.getenv("DEFAULT_FROM_EMAIL"),
        to_emails=destinatarios,
        subject=asunto,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
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
