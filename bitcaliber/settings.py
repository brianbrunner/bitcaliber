"""
Django settings for bitcalibebitcaliberr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u*#lxnz=rc0*bb-^1$8lys--hq+c%=980gf&wzs@)&a$bgotno'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'social_auth',
    'south',
    'analysis'
)

AUTH_USER_MODEL = 'analysis.GithubUser'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bitcaliber.urls'

WSGI_APPLICATION = 'bitcaliber.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'
STATICFILES_DIRS = []

# AWS Stuff

AWS_ACCESS_KEY_ID = 'AKIAJZ6URUXLRZQCWFPA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'us-east-1'
S3_BUCKET = 'bit-caliber'

# GitHub Stuff

GITHUB_APP_ID = 'e099b29298bfc7a26132'
GITHUB_API_SECRET = '9963bd1be46b3b9f97fd5b884267b49ccf08e229'
GITHUB_EXTENDED_PERMISSIONS = ['repo', 'user:email', 'write:repo_hook']

LOGIN_REDIRECT_URL = 'http://localhost:8000/'
LOGOUT_URL    = 'http://localhost:8000/logout'

SOCIAL_AUTH_LOGIN_REDIRECT_URL="http://localhost:8000/github/auth"

# RabbitMQ Celery

BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
