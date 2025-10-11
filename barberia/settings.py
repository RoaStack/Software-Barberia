"""
Django settings for barberia project.
Generado por 'django-admin startproject' usando Django 5.2.6.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url  # para manejar conexiones de base de datos en producción

# ==============================
# 📦 CARGAR VARIABLES .ENV
# ==============================
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# ==============================
# 🔐 SEGURIDAD
# ==============================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-clave-temporal")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ==============================
# 🚀 APLICACIONES INSTALADAS
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Mis apps
    'core',
    'usuarios',
    'servicios',
    'reservas',

    # Librerías externas
    'crispy_forms',
    'crispy_bootstrap5',
]

# ==============================
# ⚙️ MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'barberia.urls'

# ==============================
# 🎨 TEMPLATES
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'barberia.wsgi.application'

# ==============================
# 🧮 BASE DE DATOS
# ==============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# ==============================
# 🔑 VALIDADORES DE CONTRASEÑA
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================
# 🌍 INTERNACIONALIZACIÓN
# ==============================
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ==============================
# 🖼️ ARCHIVOS ESTÁTICOS Y MEDIA
# ==============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==============================
# 🔄 LOGIN Y AUTENTICACIÓN
# ==============================
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# ==============================
# 📧 EMAIL (para desarrollo)
# ==============================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==============================
# 🧊 CRISPY FORMS
# ==============================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==============================
# ☁️ CONFIGURACIÓN RENDER (PRODUCCIÓN)
# ==============================
if 'RENDER' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME'), '.onrender.com']

    # Seguridad HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Base de datos en Render (si existe DATABASE_URL)
    if os.getenv("DATABASE_URL"):
        DATABASES = {
            "default": dj_database_url.config(
                default=os.getenv("DATABASE_URL"),
                conn_max_age=600,
                ssl_require=True
            )
        }

    # Whitenoise para servir archivos estáticos
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================
# 🔢 ID AUTOINCREMENTAL
# ==============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
