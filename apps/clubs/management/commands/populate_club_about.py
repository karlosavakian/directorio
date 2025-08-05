
from django.core.management.base import BaseCommand
from apps.clubs.models import Club
import random

class Command(BaseCommand):
    help = "Rellena el campo 'about' de todos los clubes con descripciones ficticias"

    def handle(self, *args, **kwargs):
        textos = ['Nuestro club fue fundado hace más de 15 años con el propósito de formar deportistas íntegros, comprometidos con el esfuerzo y la disciplina que representa el boxeo. Desde entonces, hemos crecido en número de alumnos y reconocimiento en nuestra ciudad.', 'A lo largo de los años, hemos participado en torneos regionales y nacionales, obteniendo varios campeonatos y formando atletas que hoy compiten profesionalmente. Nos enorgullece mantener un ambiente de respeto, compañerismo y superación personal.', 'Contamos con entrenadores certificados y unas instalaciones modernas adaptadas para todos los niveles, desde principiantes hasta boxeadores avanzados. Nuestro objetivo es transmitir los valores del boxeo y acompañar el progreso individual de cada alumno.', 'El club tiene sus raíces en un pequeño gimnasio de barrio, donde un grupo de apasionados por el boxeo decidió enseñar lo que sabían a jóvenes de la zona. Hoy mantenemos ese mismo espíritu, pero con una estructura más profesional y con mejores recursos.', 'Además de las clases regulares, organizamos eventos comunitarios, exhibiciones, y colaboramos con escuelas y centros juveniles. Creemos que el deporte es una herramienta clave para la transformación social.']

        clubes = Club.objects.all()
        for club in clubes:
            parrafos = random.sample(textos, 3)
            club.about = "\n\n".join(parrafos)
            club.save()

        self.stdout.write(self.style.SUCCESS(f"✅ Se ha actualizado el campo 'about' para {clubes.count()} clubes."))
