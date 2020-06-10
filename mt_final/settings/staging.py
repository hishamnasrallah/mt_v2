from . import *

# Customize configurations for PROD environment
DEBUG = False

# SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=5)
# LOGGING = None
# INSTALLED_APPS.remove('django_extensions')

# AWS_ACCESS_KEY_ID = ENV.get('AWS_ACCESS_KEY_ID', None)
# AWS_SECRET_ACCESS_KEY = ENV.get('AWS_SECRET_ACCESS_KEY', None)
# AWS_STORAGE_BUCKET_NAME =  ENV.get('AWS_STORAGE_BUCKET_NAME', None)
# AWS_S3_REGION_NAME = ENV.get('AWS_S3_REGION_NAME', None)

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
