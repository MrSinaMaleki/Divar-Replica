"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='&(dj-development-secret_key)$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda hosts: hosts.split(','))


# Application definition
APPLICATIONS = ['core', 'account', 'bookmark', 'category', 'chat', 'favorite', 'post']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps:
    *list(map(lambda app: f"apps.{app}", APPLICATIONS)),

    # 3rd party apps:
    'rest_framework',
    'django_celery_beat',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'corsheaders',
]
AUTH_USER_MODEL = 'account.User'
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Divar Replica',
    'DESCRIPTION': 'A small replica of Persian popular website called Divar.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "null", 
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'config.urls'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": BASE_DIR / "file_based_cached",
        }
    }
else:
    # secure params
    SECURE_HSTS_SECONDS = 12 * 30 * 24 * 60 * 60
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = "HTTP_X_FORWARDED_PROTO", "https"
    USE_X_FORWARDED_HOST = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = "strict-origin"
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SESSION_COOKIE_AGE = 3 * 60 * 60
    SESSION_TIMEOUT = 24 * 60 * 60

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config('DB_NAME', default='postgres'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='<PASSWORD>'),
            'HOST': config('DB_HOST', default='db'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": config('REDIS_URL', str),
        }
    }


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =config('TIME_ZONE', default='UTC', cast=str)

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'storage/static/'
STATIC_ROOT_custom = BASE_DIR / 'storage/static'
if DEBUG:
    STATICFILES_DIRS = [STATIC_ROOT_custom]
else:
    STATIC_ROOT = STATIC_ROOT_custom
MEDIA_URL = 'storage/media/'
MEDIA_ROOT = BASE_DIR / 'storage/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str)
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='<PASSWORD>', cast=str)
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER', default='<EMAIL>', cast=str)

# Celery:
BROKER_URL = config('BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT =config('CELERY_ACCEPT_CONTENT', default=True, cast=lambda contents:contents.split(',') )
CELERY_TASK_SERIALIZER = config('CELERY_TASK_SERIALIZER', default='json')
CELERY_RESULT_SERIALIZER = config('CELERY_RESULT_SERIALIZER', default='json')
CELERY_TIMEZONE = config('CELERY_TIMEZONE', default='UTC')


# Django debug toolbar:
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
#
# INTERNAL_IPS = ["127.0.0.1"]

