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

# load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['localhost','127.0.0.1']
# ALLOWED_HOSTS = ['138.68.147.16', 'trosgate.com', '.trosgate.com']
# ALLOWED_HOSTS = ['gigred.website', '193.43.134.36', trosgate.great-site.net]
#  
SITE_ID = 1
SITE_DOMAIN = 'localhost'
SITE_NAME = 'Trosgate Market'
AUTH_USER_MODEL = 'account.Customer'
# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # custon Apps for trosgate site
    'daphne',
    'account',
    'control_settings',
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
    'merchants',

    # Third party apps
    'django_htmx',
    'widget_tweaks',
    'django_countries',
    'ckeditor',
    'debug_toolbar',
    # 'corsheaders',
    'rest_framework',
    'django_celery_results',
    'django_celery_beat',
    'channels',
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

MIDDLEWARE = [
    'account.middleware_host.DynamicHostMiddleware', #Must appear at the top
    # 'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",###
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Django htmx begins
    'django_htmx.middleware.HtmxMiddleware',###
    # Django htmx ends
    'account.middleware_gate.MerchantGateMiddleware', #Must appear anywhere after AuthenticationMiddleware
    'account.middleware_admin.AdminGateMiddleware', #Must appear anywhere after AuthenticationMiddleware
    'analytics.middleware.Middleware',
]


# AUTHENTICATION_BACKENDS = [
#     'account.backend.CustomAuthBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]


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
                # custom processors
                # 'account.context_processors.active_merchant',
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
ASGI_APPLICATION = 'trosgate.asgi.application'

# CHANNEL_LAYERS CONFIG
# CHANNEL_LAYERS ={
#     'default':{
#         'BACKEND':'channels_redis.core.RedisChannelLayer',
#         'CONFIG':{
#             'hosts': [('127.0.0.1', 6379)],
#         }
#     }
# }
CHANNEL_LAYERS ={
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trosgate',
        'USER': 'katey',
        'PASSWORD': 'Prof2ike.y2ky2k',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# To use Neon serverles(https//:www.neon.tech) with Django, you have to create a Project on Neon and 
# specify the project connection settings in your settings.py in 
# the same way as for standalone Postgres.

# Option 1:
# psql 'postgresql://isaacagbedam:NmDRfgF9AZ7e@ep-twilight-recipe-039780.eu-central-1.aws.neon.tech/neondb'

# Option 2:

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': 'neondb',
#     'USER': 'isaacagbedam',
#     'PASSWORD': 'NmDRfgF9AZ7e',
#     'HOST': 'ep-twilight-recipe-039780.eu-central-1.aws.neon.tech',
#     'PORT': '5432',
#   }
# }

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

# STATIC FILES PATH FOR TROSGATE SOFTWARE
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# MEDIA PATH FOR TROSGATE SOFTWARE
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
PROTECTED_MEDIA_ROOT = os.path.join(BASE_DIR, 'attachments/')
# PROTECTED_MEDIA_ROOT = BASE_DIR.parent / 'attachments'
# LOGIN AND AUTHENTICATION FOR TROSGATE SOFTWARE
LOGIN_URL = "account:login"
LOGIN_REDIRECT_URL = "account:dashboard"
LOGOUT_REDIRECT_URL = "account:homepage"

# Gmail API
# EMAIL_HOST = 'smtp-relay.brevo.com'  #'smtp-relay.sendinblue.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'myvoistudio@gmail.com'
# EMAIL_HOST_PASSWORD = '1dWKrEc3kQfRYbSD'

#Custom Email Backend for Trosgate software
EMAIL_BACKEND = 'general_settings.backends.MailerBackend'

####option one for email setup in development mode###
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

 
ADMINS = (
    ('Trosgate', 'myvoistudio@gmail.com'),
)
MANAGERS = ADMINS

# CKeditor Config
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_BASEPATH = "/static/staticfiles/ckeditor/ckeditor/"

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


# CUSTOM SESSION OBJECTS
HIRINGBOX_SESSION_ID = "proposal_box"
PROPOSALGATEWAY_SESSION_ID = "proposalgateway"
APPLICATION_SESSION_ID = "application"
APPLICATION_GATEWAY_SESSION_ID = "applicationgateway"
CONTRACT_SESSION_ID = "contract"
CONTRACT_GATEWAY_SESSION_ID = "contractgateway"

# SECURITY HEADERS - below are required in production
PASSWORD_RESET_TIMEOUT = 1209600 #two weeks in seconds
USE_THOUSAND_SEPARATOR = True
EMAIL_USE_LOCALTIME = True

# if not DEBUG:
# PREPEND_WWW = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_AGE = 1209600 #two weeks in seconds
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
EMAIL_SUBJECT_PREFIX = '[Trosgate]'

# EMAIL PASS LATEST: yqwvhebpxtgqmjph

# CELERY CONFIGURATIONS
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'  #Either this in settings file, or use as 'broker_url' variable in celery.py
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Accra' 
# STORAGE CHOICE OF CELERY TASKS
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
# CELERY BEAT CONFIGURATIONS
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# TO DETERMINE THE CODE LENGTH DURING EXTERNAL INVITATION
MAXIMUM_INVITE_SIZE = 6

# EXEMPTED PAGES IF MERCHANT IS NOT WITH ACTIVE ACCOUNT
MERCHANT_GATE_ALLOW_LIST = [
    '/',
    "/logout",
    "/marketing/support",
    "/marketing/articles",
    "/pages/how-it-works",
    "/pages/about-us",
    "/pages/terms-and-conditions",
    "/merchants/subscription",
]

# WEBROOT_PATH = '/home/www/letsencrypt'

CACHE_TTL = 60 * 60 # 1 HOUR CACHE TIMEHOUT
