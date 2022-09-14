"""
Django settings for trosgate project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '45.79.17.59'] 
# '127.0.0.1', 'localhost'

AUTH_USER_MODEL = 'account.Customer'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custon Apps for trosgate site
    'account',
    'general_settings',
    'freelancer',
    'client',
    'analytics',
    'projects',
    'proposals',
    'teams',
    'contract',
    'quiz',
    'pages',
    'marketing',
    'transactions',
    'notification',
    'applications',
    'future',
    'resolution',
    'payments',

    # Third party apps
    'django_htmx',
    'widget_tweaks',
    'django_countries',
    'ckeditor',
    # 'mptt',
    # 'channels',
    # 'embed_video',
    # 'django_celery_results',
    # 'django_celery_beat',
    # Two factor Authentication
    
    'django_otp',
    'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',
    # 'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Two factor Authentication middleware
    'django_otp.middleware.OTPMiddleware',
    # Django htmx begins
    'django_htmx.middleware.HtmxMiddleware',
    # Django htmx ends
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'analytics.middleware.Middleware',
]

ROOT_URLCONF = 'trosgate.urls'

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
                # for embed video
                'django.template.context_processors.request',
                # custom processors
                'proposals.context_processors.published_proposal',
                'teams.context_processors.active_team',
                'general_settings.context_processors.categories',
                'general_settings.context_processors.website',
                'general_settings.context_processors.autoLogoutSystem',
                'transactions.context_processors.hiring_box',
                'applications.context_processors.application_addon',
                'contract.context_processors.chosen_contract', 
                'future.context_processors.future_release', 
            ],
        },
    },
]

WSGI_APPLICATION = 'trosgate.wsgi.application'
# ASGI_APPLICATION = 'trosgate.asgi.application'


# in place of redis while on windows in development environment
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trosgate',
        'USER': 'katey',
        'PASSWORD': 'Prof2ike.y2ky2k',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# this will keep files on server
STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# This saves a copy of files on local pc
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ENV_PATH = os.path.dirname(BASE_DIR)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(ENV_PATH, 'media')

LOGIN_URL = "account:login"
LOGIN_REDIRECT_URL = "account:dashboard"

#Custom Email Backend for this software
EMAIL_BACKEND = 'general_settings.backends.MailerBackend'


### option two for email setup in development mode ###
# I am using gmail setup

####option one for email setup in development mode###
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

####option two for email setup in development mode###
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'myvoistudio@gmail.com'
# EMAIL_HOST_PASSWORD = 'kadjbfgubatoipur'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_EMAIL_FROM = 'Trosgate <myvoistudio@gmail.com>'



ADMINS = (
    ('Trosgate', 'voistudio@gmail.com'),
)
MANAGERS = ADMINS

# CKeditor Config
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_BASEPATH = "/static/static_root/ckeditor/ckeditor/"

CKEDITOR_CONFIGS = {
    'default': {
        'width': '100%',
        'tabSpaces': 4,
    }
}

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
}

# CELERY CONFIGURATIONS
### CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
# accept_content = ['application/json']
# result_serializer = 'json'
# task_serializer = 'json'
### default timezone is "UTC". Activate this if you want a different timzone ###
timezone = 'UTC'
# timezone = 'Africa/Accra'

# STORAGE CHOICE OF CELERY TASKS
# result_backend = 'django-db'

# CELERY BEAT CONFIGURATIONS
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# CUSTOM SESSIONS

HIRINGBOX_SESSION_ID = "proposal_box"
PROPOSALGATEWAY_SESSION_ID = "proposalgateway"
APPLICATION_SESSION_ID = "application"
APPLICATION_GATEWAY_SESSION_ID = "applicationgateway"
CONTRACT_SESSION_ID = "contract"
CONTRACT_GATEWAY_SESSION_ID = "contractgateway"


# SECURE HEADERS - below are required in production
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_AGE = 1209600 #two weeks in seconds
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# CSRF_COOKIE_SECURE = True