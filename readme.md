## Puesta en marcha

1. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows usa 'venv\\Scripts\\activate'
pip install -r requirements.txt
```

2. Aplica las migraciones de la base de datos:
```bash
python manage.py migrate
```

3. Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```
   Si ejecutas el servidor desde un dominio distinto (por ejemplo, en
   servicios en la nube o IDEs remotos), asegúrate de incluir esa URL en la
   variable de entorno `CSRF_TRUSTED_ORIGINS`:
```bash
export CSRF_TRUSTED_ORIGINS="https://tu-dominio.example.com"
```
4. Configura los proveedores sociales (Google o Facebook) en el panel de
   administración dentro de "Social applications". Guarda las credenciales
   correspondientes y ejecuta `python manage.py migrate` para aplicar las
   tablas de `django-allauth`.


El sitio quedará disponible en http://127.0.0.1:8000/.


## Instalación de dependencias

Para instalar las dependencias en un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Las pruebas requieren Django y Pillow, ya incluidos en `requirements.txt`.




directorio_boxeo/
│
├── apps/
│   ├── clubs/
│   │   ├── admin.py                 -> Configuración de Django Admin para el modelo Club y relacionados.
│   │   ├── apps.py                  -> Configuración de la app en Django.
│   │   ├── forms.py                 -> Formularios de reseñas y clubes.
│   │   ├── urls.py                  -> Enrutamiento de URLs para la app clubs.
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py          -> Importación centralizada de modelos.
│   │   │   ├── club.py              -> Modelo para Club y ClubPhoto.
│   │   │   ├── reseña.py            -> Modelo para las reseñas de los clubes.
│   │   │   ├── horario.py           -> Modelo para horarios de clases en un club.
│   │   │   ├── competidor.py        -> Modelo para gestionar competidores.
│   │   │   └── clase.py             -> Modelo para gestionar clases dentro de un club.
│   │   │
│   │   ├── views/
│   │   │   ├── __init__.py          -> Importación centralizada de vistas.
│   │   │   ├── dashboard.py         -> Vistas para el panel de administración de un club.
│   │   │   ├── public.py            -> Vistas públicas para navegación y detalle de clubes.
│   │   │   ├── search.py            -> Vistas para realizar búsquedas de clubes.
│   │   │   ├── (las vistas de reseñas se movieron a `apps/users/views/review.py`).
│   │   │
│   │   └── migrations/              -> Migraciones de base de datos para los modelos de clubs.
│   │
│   ├── core/
│   │   ├── urls.py                  -> Enrutamiento principal de la app.
│   │   ├── views.py                 -> Vistas generales de la aplicación.
│   │   ├── models.py                -> Modelos generales (si se requieren en el futuro).
│   │   ├── services/                -> Lógica de servicios (e.g. enviar emails, servicios externos).
│   │   ├── templatetags/            -> Carga de etiquetas y filtros personalizados para templates.
│   │   └── utils/                   -> Utilidades generales para lógica compartida.
│   │
│   └── users/
│       ├── admin.py                 -> Configuración del admin para usuarios y perfiles.
│       ├── apps.py                  -> Configuración de la app en Django.
│       ├── forms.py                 -> Formularios de login, registro y perfiles.
│       ├── urls.py                  -> Enrutamiento de URLs para la app users.
│       │
│       ├── models/
│       │   ├── __init__.py          -> Importación centralizada de modelos.
│       │   └── user.py              -> Modelo extendido de usuario.
│       │
│       ├── views/
│       │   ├── __init__.py          -> Importación centralizada de vistas.
│       │   ├── auth.py              -> Vistas de autenticación (login, logout, registro).
│       │   ├── public.py            -> Vistas públicas relacionadas con usuarios.
│       │   └── review.py            -> Vistas para gestionar reseñas (crear, editar, eliminar).
│       │
│       └── migrations/              -> Migraciones de base de datos para los modelos de users.
│
├── config/
│   ├── __init__.py                  -> Inicialización del proyecto Django.
│   ├── settings.py                  -> Configuración general del proyecto.
│   ├── urls.py                      -> Enrutamiento principal del proyecto.
│   ├── wsgi.py                      -> Configuración para WSGI (deploy).
│   └── asgi.py                      -> Configuración para ASGI (WebSockets).
│
├── templates/
│   ├── clubs/                       -> Templates para visualización de clubes.
│   ├── core/                        -> Templates para páginas principales (Home, About, etc.).
│   ├── users/                       -> Templates para autenticación (login, registro).
│   └── partials/                    -> Templates parciales (_header, _footer, _search_form).
│
├── static/
│   ├── css/                         -> Hojas de estilo CSS.
│   ├── js/                          -> Archivos JavaScript.
│   └── img/                         -> Imágenes del proyecto.
│
├── media/                           -> Archivos multimedia subidos por los usuarios.
│
├── manage.py                        -> Script de Django para tareas administrativas.
│
└── requirements.txt                 -> Dependencias del proyecto.
 
