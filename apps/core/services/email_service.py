# apps/core/services/email_service.py
from django.core.mail import send_mail

def send_welcome_email(user_email):
    """ Envía un correo de bienvenida """
    send_mail(
        'Bienvenido a Clubs de Boxeo',
        'Gracias por unirte a nuestra comunidad.',
        'noreply@clubsdeboxeo.com',
        [user_email],
        fail_silently=True,


def send_confirmation_email(user_email):
    """Envía un correo de confirmación de registro"""
    send_mail(
        'Registro completado',
        'Tu cuenta ha sido creada exitosamente.',
        'noreply@clubsdeboxeo.com',
        [user_email],
        fail_silently=True,
