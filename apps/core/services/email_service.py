# apps/core/services/email_service.py
from django.core.mail import send_mail

def send_welcome_email(user_email):
    """ Envía un correo de bienvenida """
    send_mail(
        'Bienvenido a Clubs de Boxeo',
        'Gracias por unirte a nuestra comunidad.',
        'noreply@clubsdeboxeo.com',
        [user_email],
        fail_silently=False,
    )
