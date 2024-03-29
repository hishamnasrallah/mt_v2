"""
Django settings for mt_final project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*6+a5*zg(x2pgd1##n=0yeehpb$%#6*)fzr)frs0&o))emw#ux'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'suit',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_select2',
    'crispy_forms',
    'translation',
    'colorfield',
    'import_export',
    'ckeditor',
    'colorful',
    'channels',
]
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'example_channels.routing.channel_routing',
    }
}
IMPORT_EXPORT_USE_TRANSACTIONS = True

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type'
]


ROOT_URLCONF = 'mt_final.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'registration')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'translation.context_processors.client_logo',
            ],
        },
    },
]
CRISPY_TEMPLATE_PACK = 'bootstrap3'

WSGI_APPLICATION = 'mt_final.wsgi.application'
ASGI_APPLICATION = 'mt_final.routing.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hishamapp5',
        'USER': 'postgres',
        'PASSWORD': 'AMw3N$129#$',
        'HOST': 'mt.cnp7tmhwgmei.us-east-1.rds.amazonaws.com',
        'PORT': 5432,
    }
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


SEGMENTATION_ENDPOINT_AR = os.environ.get("SEGMENTATION_ENDPOINT_AR", "http://127.0.0.1:1200/api/segmented_translation")
SEGMENTATION_ENDPOINT_EN = os.environ.get("SEGMENTATION_ENDPOINT_EN", "http://127.0.0.1:1300/api/segmented_translation")
MT_ENDPOINT_AR_EN = os.environ.get("MT_ENDPOINT_AR_EN", "http://172.31.92.25:7777/translate")
MT_ENDPOINT_EN_AR = os.environ.get("MT_ENDPOINT_EN_AR", "http://18.185.138.246:7777/translate")
FORCE_SCRIPT_NAME = os.environ.get("FORCE_SCRIPT_NAME", "")
JSON_AS_ASCII = os.environ.get("JSON_AS_ASCII", 0)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

CELERY_BROKER_URL = 'redis://localhost:6379'

CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = FORCE_SCRIPT_NAME + '/static/'
CUSTOM_STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = FORCE_SCRIPT_NAME + '/media/'
CUSTOM_MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]



PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

LOGIN_REDIRECT_URL = FORCE_SCRIPT_NAME + '/'
LOGOUT_REDIRECT_URL = FORCE_SCRIPT_NAME + '/accounts/login/'
LOGIN_URL = FORCE_SCRIPT_NAME + '/accounts/login/'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '[%(levelname)s] %(asctime)s %(module)s %(process)d %(thread)d : %(message)s \n',
#             'datefmt': "%d/%b/%Y %H:%M:%S",
#         },
#     },
#     'handlers': {
#         # Log to a text file
#         'logfile': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': f'{os.getcwd()}/media/testlog.log',
#             'formatter': 'verbose',
#         },
#         # 'hf_logfile': {
#         #     'class': 'logging.handlers.RotatingFileHandler',
#         #     'filename': f'{os.getcwd()}/media/testlog1.log',
#         #     'formatter': 'verbose',
#         # },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['logfile'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['logfile'],
#             'propagate': True,
#         },
#         'django.server': {
#             'handlers': ['logfile'],
#             'propagate': True,
#         },
#         # 'HF': {
#         #     'handlers': ['hf_logfile'],
#         #     'propagate': True,
#         #     'level': 'INFO'
#         # },
#     },
# }
