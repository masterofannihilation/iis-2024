from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

###############################################################################
### Deployment related settings
###############################################################################

# Set these environment variables on production server!!!
# SECRET_KEY=<secure_key>
# DEBUG=False
# ALLOWED_HOSTS=<domain_of_the_web_service>
# SEED_USER_PWD=<default_password_of_seeded_users>
# DATABASE_URL=<see dj_database_url usage>

# Set SECRET_KEY in production!
_development_key = "django-insecure-$(!hr+2ddrbr^o75u5q0d(8immx-jfcmg)##o7mh4j3%h%^_bx"
SECRET_KEY = os.getenv("SECRET_KEY", _development_key)

# By default run in debug mode otherwise set DEBUG=False
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = []
_hosts_list = os.getenv("ALLOWED_HOSTS", None)
if _hosts_list:
    ALLOWED_HOSTS = _hosts_list.split(",")

if not DEBUG:
    # Enforce HTTPS communication
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Always redirect to HTTPS
    SECURE_SSL_REDIRECT = True

    # Transmit cookies only over HTTPS
    SESSION_COOKIE_SECURE = True

    # Against Cross-Site Request Forgery
    CSRF_COOKIE_SECURE = True

USE_POSTGRESQL = os.getenv("USE_POSTGRESQL", "False") == "True" or not DEBUG

ALLOW_WEAK_PWD = os.getenv("ALLOW_WEAK_PWD", "True") == "True"

###############################################################################
### Application definition
###############################################################################

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "shelter",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_auto_logout.middleware.auto_logout",
]

ROOT_URLCONF = "animal_shelter.urls"

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
                "shelter.context_processors.logged_in_user",
            ],
        },
    },
]

WSGI_APPLICATION = "animal_shelter.wsgi.application"


###############################################################################
### Database settings
###############################################################################

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if USE_POSTGRESQL or os.getenv("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            env="DATABASE_URL",
            default="postgres://user:password@localhost:5432/shelter",  # Dockerfile database
        )
    }

###############################################################################
### Password validation
###############################################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

if ALLOW_WEAK_PWD:
    AUTH_PASSWORD_VALIDATORS = []  # Disables all password validators

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "animal_shelter/static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SEED_DEMO_DATA = True
SEED_USER_PWD = os.getenv("SEED_USER_PWD", "password")

AUTH_USER_MODEL = "shelter.User"
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

AUTO_LOGOUT = {
    "SESSION_TIME": 10 * 60,  # 10 minutes
    "MESSAGE": "You have been automatically logged out due to inactivity.",
}
