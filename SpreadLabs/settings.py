"""
    SpreadLabs - Social media suite
    Copyright (C) 2015  Christopher Mejia Montoya - me@chrissmejia.com - chrissmejia.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, socket
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&v6@7!$*^uzs9nh^&w14^9s=^vv#qi94j17%$-ff7jfopfrlnq' # change  this key

DEBUG = False
ONLINE = True

COMPRESS_ENABLED = True
COMPRESS_TEMPLATE_FILTER_CONTEXT = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Christopher Mejia', 'christopher@spreadlabs.com'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ses',
    'django_nvd3',
    "compressor",
    'accounts',
    'apps',
    'appsExtended',
    'asap',
    'dashboard',
    'dashboardExtended',
    'errors',
    'facebook',
    'records',
    'recordsExtended',
    'stats',
    'statsExtended',
    'clients.app',
    'clients.asap_to',
    'web',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'SpreadLabs.multihost.MultiHostMiddleware',
)

HOST_MIDDLEWARE_URLCONF_MAP = {
    "localhost": "SpreadLabs.urls.urls",
    "spreadlabs.com": "SpreadLabs.urls.urls",
    "asap.to": "SpreadLabs.urls.urls",
}

ROOT_URLCONF = 'SpreadLabs.urls.clients'

WSGI_APPLICATION = 'SpreadLabs.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#Fill the database information
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',                                # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                                         # Set to empty string for default.
    }
}

## Email Settings
EMAIL_BACKEND = 'django_ses.SESBackend'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_SES_ACCESS_KEY_ID = ''
AWS_SES_SECRET_ACCESS_KEY = ''

DEFAULT_FROM_EMAIL = 'SpreadLabs Bot <no-reply@spreadlabs.com>'

#Facebook app permissions
if not ONLINE:
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET_KEY = ''
else:
    FACEBOOK_APP_ID = ''
    FACEBOOK_APP_SECRET_KEY = ''
FACEBOOK_INITIAL_SCOPE = 'read_insights, manage_pages'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-cr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MAIN_DIR = BASE_DIR + "/SpreadLabs"
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = MAIN_DIR + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
if not ONLINE:
    MEDIA_URL = 'http://spreadlabs.dev/SpreadLabs/SpreadLabs/media/'
else:
    MEDIA_URL = 'https://spreadlabs.com/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = MAIN_DIR + '/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
if not ONLINE:
    STATIC_URL = 'http://spreadlabs.dev/SpreadLabs/SpreadLabs/static/'
else:
    STATIC_URL = 'https://spreadlabs.com/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.eggs.Loader',
)

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT =  STATIC_ROOT

COMPRESS_JS_FILTERS = [
    'compressor.filters.template.TemplateFilter',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True

# Get profile
AUTH_PROFILE_MODULE = 'accounts.Profile'

# @login_required
LOGIN_URL = '/dashboard/accounts/login/'