"""
Django settings for AI_Agent_Config project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = []


# Application definition

INSTALLED_APPS = [
    # 'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'assistant',

#========== 3RD PARTY LIBRARIES =======
    'channels',
    'channels_redis',
    'rest_framework',
    'rest_framework.authtoken',
#------------- payments --------------
    'djstripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AI_Agent_Config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI_APPLICATION = 'AI_Agent_Config.wsgi.application'
ASGI_APPLICATION = 'AI_Agent_Config.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'HOST': os.environ['DATABASE_HOST'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'PORT': os.environ['DATABASE_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ['REDIS_HOST']],
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}


#======================STRIPE CONFIG====================================
# Dj stripe config
# Stripe keys (use test keys in development)
STRIPE_LIVE_MODE = False  # Set True in production
STRIPE_TEST_PUBLIC_KEY = os.environ['STRIPE_TEST_PUBLIC_KEY']
STRIPE_TEST_SECRET_KEY = os.environ['STRIPE_TEST_SECRET_KEY']
STRIPE_LIVE_PUBLIC_KEY = os.environ['STRIPE_LIVE_PUBLIC_KEY']
STRIPE_LIVE_SECRET_KEY = os.environ['STRIPE_LIVE_SECRET_KEY']

# Use test keys for development:
STRIPE_PUBLIC_KEY = STRIPE_TEST_PUBLIC_KEY
STRIPE_SECRET_KEY = STRIPE_TEST_SECRET_KEY

DJSTRIPE_WEBHOOK_SECRET = os.environ['STRIPE']
DJSTRIPE_USE_NATIVE_JSONFIELD = True

# dj-stripe settings
DJSTRIPE_WEBHOOK_URL = "https://your-domain.com/stripe/webhook/"

# Optional: Specify which Stripe model field to use for foreign keys
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

#=======================================================================


# Celery Configuration
CELERY_BROKER_URL = os.environ['REDIS_HOST']
CELERY_RESULT_BACKEND = os.environ['REDIS_HOST']
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"



from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'check-due-fb-post-every-minute': {
        'task': 'assistant.tasks.check_due_facebook_post',
        'schedule': crontab(minute='*'), # Runs every minute
    }
}

CELERY_BEAT_SCHEDULE = {
    'check-due-ig-post-every-minute': {
        'task': 'assistant.tasks.check_due_instagram_post',
        'schedule': crontab(minute='*'), # Runs every minute
    }
}

CELERY_BEAT_SCHEDULE = {
    'check-due-in-post-every-minute': {
        'task': 'assistant.tasks.check_due_linkedin_post',
        'schedule': crontab(minute='*'), # Runs every minute
    }
}

CELERY_BEAT_SCHEDULE = {
    'check-due-x-post-every-minute': {
        'task': 'assistant.tasks.check_due_twitter_post',
        'schedule': crontab(minute='*'), # Runs every minute
    }
}



SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']

SOCIAL_AUTH_TWITTER_KEY = os.environ['SOCIAL_AUTH_TWITTER_KEY']
SOCIAL_AUTH_TWITTER_SECRET = os.environ['SOCIAL_AUTH_TWITTER_SECRET']

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.environ['SOCIAL_AUTH_LINKEDIN_KEY']
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_LINKEDIN_SECRET']

SOCIAL_AUTH_INSTAGRAM_KEY = os.environ['SOCIAL_AUTH_INSTAGRAM_KEY']
SOCIAL_AUTH_INSTAGRAM_SECRET = os.environ['SOCIAL_AUTH_INSTAGRAM_SECRET']


HUBSPOT_CLIENT_ID = os.environ['HUBSPOT_CLIENT_ID']
HUBSPOT_CLIENT_SECRET = os.environ['HUBSPOT_CLIENT_SECRET']
HUBSPOT_REDIRECT_URI = 'your-redirect-uri'
HUBSPOT_BASE_URL = 'https://api.hubapi.com'