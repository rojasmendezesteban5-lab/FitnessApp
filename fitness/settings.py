"""
Django settings for fitness project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# SEGURIDAD
# =========================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "clave-temporal-solo-para-desarrollo"
)

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    os.environ.get(
        "RENDER_EXTERNAL_HOSTNAME",
        "fitnessapp-ernl.onrender.com"
    ),
]


# =========================================================
# APLICACIONES
# =========================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]


# =========================================================
# MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "fitness.urls"


# =========================================================
# PLANTILLAS
# =========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "fitness.wsgi.application"


# =========================================================
# BASE DE DATOS
# =========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =========================================================
# VALIDACIÓN DE CONTRASEÑAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
]


# =========================================================
# IDIOMA Y ZONA HORARIA
# =========================================================

LANGUAGE_CODE = "es"

TIME_ZONE = "America/Costa_Rica"

USE_I18N = True

USE_TZ = True


# =========================================================
# ARCHIVOS ESTÁTICOS
# =========================================================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# =========================================================
# CORREO
# =========================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# =========================================================
# LOGIN
# =========================================================

LOGIN_URL = "/login/"