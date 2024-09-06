"""
Django settings for staffnetapi project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(".env")

if not os.path.isfile(ENV_PATH):
    raise FileNotFoundError("The env file was not found.")

load_dotenv(ENV_PATH)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]


def str_to_bool(value: str) -> bool:
    """Convert a string to a boolean."""
    return value.lower() in ("true", "t", "1")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(os.environ["DEBUG"])

ALLOWED_HOSTS = [host.strip() for host in os.environ["ALLOWED_HOSTS"].split(",")]

# ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_auth_ldap",
    "administration",
    "employees",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# if not "test" in sys.argv:
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    host.strip() for host in os.environ["CSRF_TRUSTED_ORIGINS"].split(",")
]


if not DEBUG:
    cors_allowed_origins = os.environ["CORS_ALLOWED_ORIGINS"]
    # This avoid the error of having an empty string as an allowed host (This is a security risk)
    CORS_ALLOWED_ORIGINS = (
        [cors.strip() for cors in cors_allowed_origins.split(",")]
        if cors_allowed_origins
        else []
    )

ROOT_URLCONF = "staffnetapi.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "staffnetapi.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "NAME": "staffnet2",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]

AUTHENTICATION_BACKENDS = [
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# LDAP configuration
AUTH_LDAP_SERVER_URI = "ldap://CYC-SERVICES.COM.CO:389"
AUTH_LDAP_BIND_DN = "CN=StaffNet,OU=TECNOLOGÍA,OU=BOGOTA,DC=CYC-SERVICES,DC=COM,DC=CO"
AUTH_LDAP_BIND_PASSWORD = os.getenv("AdminLDAPPassword")

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch(
        "OU=BOGOTA,DC=CYC-SERVICES,DC=COM,DC=CO",  # Search base
        ldap.SCOPE_SUBTREE,  # Search scope
        "(&(objectClass=user)(sAMAccountName=%(user)s))",  # Search filter
    ),
    LDAPSearch(
        "OU=MEDELLIN,DC=CYC-SERVICES,DC=COM,DC=CO",  # Search base
        ldap.SCOPE_SUBTREE,  # Search scope
        "(&(objectClass=user)(sAMAccountName=%(user)s))",  # Search filter
    ),
    LDAPSearch(
        "OU=BUCARAMANGA,DC=CYC-SERVICES,DC=COM,DC=CO",  # Search base
        ldap.SCOPE_SUBTREE,  # Search scope
        "(&(objectClass=user)(sAMAccountName=%(user)s))",  # Search filter
    ),
    LDAPSearch(
        "OU=VILLAVICENCIO,DC=CYC-SERVICES,DC=COM,DC=CO",  # Search base
        ldap.SCOPE_SUBTREE,  # Search scope
        "(&(objectClass=user)(sAMAccountName=%(user)s))",  # Search filter
    ),
)

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
}

AUTH_LDAP_ALWAYS_UPDATE_USER = False

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "es-CO"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

log_dir = os.path.join(BASE_DIR, "utils", "logs")
# Create another log file for each minute
now = datetime.now()
year_month = now.strftime("%Y-%B")
month = now.strftime("%B")
# Create the log file
if not os.path.exists(os.path.join(log_dir, year_month)):
    os.makedirs(os.path.join(log_dir, year_month))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "time-lvl-msg": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
        "response_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_dir, year_month, f"requests_{month}.log"),
            "formatter": "time-lvl-msg",
        },
        "exception_file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(log_dir, "exceptions.log"),
            "formatter": "time-lvl-msg",
        },
    },
    "loggers": {
        "requests": {
            "handlers": ["response_file", "exception_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "console": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["exception_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django_auth_ldap": {
            "handlers": ["console", "response_file", "exception_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["exception_file"],
        "level": "ERROR",
    },
}
