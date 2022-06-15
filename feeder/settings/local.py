from feeder.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f00r*pf@%#^^k=jnah3*n(!zniam9&@nj$may-9*w=p(hvnv*s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
PRODUCT_STORAGE_CLASS = "django.core.files.storage.FileSystemStorage"

VOIP_SERVER_TOKEN = "asdj1ASDJK213asdkljc123ASDasd"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.spatialite",
        "NAME": os.path.join(os.path.dirname(BASE_DIR), "db.sqlite3"),
    }
}

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
INTERNAL_IPS = ["127.0.0.1"]


CELERY_TASK_ALWAYS_EAGER = True
CELERY_ALWAYS_EAGER = True

SITE_ID = 1
