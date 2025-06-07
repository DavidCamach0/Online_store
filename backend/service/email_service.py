# Escritorio/GIT/backend/service/email_service.py
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def enviar_email_confirmacion(destinatario, token):
    confirm_url = f"{os.getenv('FRONTEND_CONFIRM_URL')}?token={token}"

    contenido_html = f"""
    <h1>Bienvenido a la tienda</h1>
    <p>Hacé clic en el siguiente enlace para confirmar tu cuenta:</p>
    <a href="{confirm_url}">Confirmar cuenta</a>
    """

    mensaje = Mail(
        from_email='victorcamacho10722@gmail.com',
        to_emails=destinatario,
        subject='Confirmación de cuenta',
        html_content=contenido_html
    )

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        sg.send(mensaje)
    except Exception as e:
        print(f"Error al enviar correo: {e}")
