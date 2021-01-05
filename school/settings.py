"""
Django settings for school project.
Generated by 'django-admin startproject' using Django 2.2.3.
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import django_heroku
import dj_database_url
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_env_variable('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['classbop.herokuapp.com', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # <--


    'allauth',  # <--
    'allauth.account',  # <--
    'allauth.socialaccount',  # <--
    'allauth.socialaccount.providers.google',  # <--
    'apps.students.apps.StudentsConfig',
    'apps.teachers.apps.TeachersConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.users.apps.UsersConfig',
    'crispy_forms',
]

# For Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'classbopteam@gmail.com'
    EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_PASSWORD')

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_FAIL_SILENTLY = not DEBUG

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

ROOT_URLCONF = 'school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'school.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {}

if DEBUG:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_school',
        'USER': 'postgres',
        'PASSWORD': 'Pistons1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
else:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'graph_data_cache',
        'TIMEOUT': 900,
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

DEBUG_PROPAGATE_EXCEPTIONS = True

AUTH_USER_MODEL = 'users.User'

# Login url info
LOGIN_URL = 'login'

django_heroku.settings(locals())

AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend',
 )

SITE_ID = 5
LOGIN_REDIRECT_URL = 'external_login'
ACCOUNT_SIGNUP_REDIRECT_URL = 'finish_registration'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ACCOUNT_FORMS = {
    'signup': 'users.forms.SocialRegistrationForm',
}
