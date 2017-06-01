"""
Django settings for bcpp_clinic project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import configparser
import os
from unipath import Path
import sys


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

APP_NAME = 'bcpp_clinic'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*3izpxc9!j7)(a*2+_sw%_10gx*_$z1-%bf2mz%!pkd%@*%$1)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'edc_offstudy',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_dashboard.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'bcpp.apps.AppConfig',
    'bcpp.apps.EdcBaseAppConfig',
    'bcpp.apps.EdcLabAppConfig',
    'bcpp.apps.EdcLabelAppConfig',
    'bcpp_clinic.apps.EdcMetadataAppConfig',
    'bcpp.apps.EdcIdentifierAppConfig',
    'bcpp.apps.EdcProtocolAppConfig',
    'bcpp.apps.SurveyAppConfig',
    'bcpp.apps.EdcMapAppConfig',
    'bcpp.apps.EdcConsentAppConfig',
    'bcpp.apps.EdcDeviceAppConfig',
    'bcpp.apps.EdcBaseTestAppConfig',
    'bcpp.apps.EdcTimepointAppConfig',
    'bcpp.apps.EdcAppointmentAppConfig',
    'bcpp_clinic.apps.EdcVisitTrackingAppConfig',
    'bcpp.apps.HouseholdAppConfig',
    'bcpp.apps.MemberAppConfig',
    'bcpp.apps.EnumerationAppConfig',
#     'bcpp.apps.BcppSubjectAppConfig',
    'bcpp.apps.BcppFollowAppConfig',
    'bcpp.apps.PlotAppConfig',
    'bcpp.apps.EdcSyncAppConfig',
    'bcpp.apps.EdcSyncFilesAppConfig',
    'bcpp_report.apps.AppConfig',
    'bcpp_clinic.apps.AppConfig',
]


if 'test' in sys.argv:
    MIGRATION_MODULES = {
        "django_crypto_fields": None,
        "edc_call_manager": None,
        "edc_appointment": None,
        "edc_call_manager": None,
        "edc_consent": None,
        "edc_death_report": None,
        "edc_export": None,
        "edc_identifier": None,
        "edc_metadata": None,
        "edc_registration": None,
        "edc_sync": None,
        'edc_map': None,
        "bcpp": None,
        "bcpp_subject": None,
        "plot": None,
        "household": None,
        "member": None,
        "survey": None,
        'admin': None,
        "auth": None,
        "edc_sync_files": None,
        'sessions': None,
    }

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bcpp_clinic.urls'

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

WSGI_APPLICATION = 'bcpp_clinic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
ETC_DIR = '/etc'
CONFIG_FILE = '{}.conf'.format('bcpp')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, APP_NAME, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, APP_NAME, 'media')

MEDIA_URL = '/media/'

GIT_DIR = BASE_DIR.ancestor(1)

KEY_PATH = '/Volumes/crypto_keys'

CONFIG_FILE = '{}.conf'.format('bcpp')

CONFIG_PATH = os.path.join(ETC_DIR, 'bcpp', CONFIG_FILE)

config = configparser.RawConfigParser()
config.read(os.path.join(CONFIG_PATH))

CURRENT_MAP_AREA = 'test_community'
DEVICE_ID = config['edc_device'].get('device_id', '99')
DEVICE_ROLE = config['edc_device'].get('role')
LABEL_PRINTER = config['edc_label'].get('label_printer', 'label_printer')
SURVEY_GROUP_NAME = config['survey'].get('group_name')
SURVEY_SCHEDULE_NAME = config['survey'].get('schedule_name')
ANONYMOUS_ENABLED = config['bcpp'].get('anonymous_enabled')
DEVICE_IDS = [d.strip() for d in config['edc_map'].get('device_ids').split(',')]
