from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# TODO SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tgu5-ltipum7#tjb(77%_j(fk74p^8e*3sxoov&lk6wpc*i7@^'
# TODO SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]  # ['[::1]', 'localhost', '0.0.0.0']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bugTracker.apps.BugtrackerConfig',
    'core.apps.CoreConfig',
    'rest_framework',
    'taggit',
    'drf_yasg'
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ]
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pythBugTracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')]
        ,
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

WSGI_APPLICATION = 'pythBugTracker.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

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
############################################################################################################
############################################################################################################
############################################################################################################
# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': str(BASE_DIR / 'debug.log'),
        },
    },
    'loggers': {
        'bugtracker': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
}
############################################################################################################
############################################################################################################
############################################################################################################
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
############################################################################################################
############################################################################################################
############################################################################################################
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "/auth/login"
LOGOUT_REDIRECT_URL = LOGIN_URL
LOGIN_REDIRECT_URL = "/"
AUTH_USER_MODEL = "core.CustomUser"
############################################################################################################
############################################################################################################
############################################################################################################
# STATIC AND MEDIA FILES

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'public')
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [str(BASE_DIR / 'static'), ]
MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / '_media')
############################################################################################################
############################################################################################################
############################################################################################################
# EMAIL SETTINGS
ADMINS = [('BugTracker', 'noreply.bugtracker@sankore.com'), ('Ik', 'ikechukwu@sankore.com')]
# email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # TODO Change this to smtp.EmailBacked for maintesting
DEFAULT_FROM_EMAIL = "noreply.bugtracker@sankore.com"
EMAIL_HOST = ""
EMAIL_PORT = ""
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = ""
EMAIL_USE_SSL = ""
EMAIL_TIMEOUT = ""
EMAIL_SSL_KEYFILE = ""
EMAIL_SSL_CERTFILE = ""
MAIL_TEMPLATE_ROOT = str(BASE_DIR / "resources")
# The SMTP backend is the default configuration inherited by Django.
# If you want to specify it explicitly, put the following in your settings:
############################################################################################################
