"""
Django settings for barberia project.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
load_dotenv(BASE_DIR / ".env")

# 🔐 SECRET_KEY y DEBUG
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-temporal')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['software_barberia.onrender.com','localhost', '127.0.0.1',]

# ------------------- APLICACIONES -------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tus apps
    'core',
    'usuarios',
    'servicios',
    'reservas',

    # Librerías externas
    'crispy_forms',
    'crispy_bootstrap5',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

# ------------------- MIDDLEWARE -------------------
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

# ------------------- BASE DE DATOS -------------------
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

# ------------------- VALIDACIONES -------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------- LOCALIZACIÓN -------------------
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# ------------------- ARCHIVOS ESTÁTICOS -------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ------------------- ARCHIVOS MEDIA -------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------- AUTENTICACIÓN -------------------
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'usuarios:dashboard'
LOGOUT_REDIRECT_URL = 'core:home'

# ------------------- EMAIL -------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# ------------------- CRISPY FORMS -------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ------------------- CLOUDINARY -------------------
# Si usas CLOUDINARY_URL (recomendado), NO necesitas CLOUDINARY_STORAGE = { ... }
# Render leerá directamente la variable CLOUDINARY_URL
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ------------------- CONFIGURACIÓN RENDER -------------------
if 'RENDER' in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = [os.getenv('RENDER_EXTERNAL_HOSTNAME'), 'tu-app.onrender.com']

    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    if os.getenv("DATABASE_URL"):
        DATABASES = {
            "default": dj_database_url.config(
                default=os.environ["DATABASE_URL"],
                conn_max_age=600,
                ssl_require=True
            )
        }

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
